import plotly.graph_objects as go
import plotly.express as px
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd


# Define function to convert list to tuple for SQL query
def query_tuple(list_):
    return str(tuple(list_)).replace(',)', ')')

# Define function to create hospitals map
def create_hospital_map_new(df_hospitals, mapstyle, chart_colors):
    # define colorscales
    colorscales = ['Blugrn', 'Purp', 'Peach', 'Brwnyl']

    fig = go.Figure()

    # Create layers with hospitals
    k = 0
    for provider_type in df_hospitals['provider_type_code'].unique():
        
        # Filter the dataframe for the current provider type
        df_hospitals_filtered = df_hospitals.loc[df_hospitals['provider_type_code'] == provider_type]

        # Normalize the marker sizes
        min_beds = 10
        max_beds = 1000
        min_size = 4
        max_size = 25
        normalized_sizes = (df_hospitals_filtered['beds_number'] - min_beds) / (max_beds - min_beds) * (max_size - min_size) + min_size

        # Create layers for each provider type
        layer = go.Scattermapbox(
            lat=df_hospitals_filtered['latitude'],
            lon=df_hospitals_filtered['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=normalized_sizes,  # Scaled size of the markers
                color=chart_colors[provider_type],  # Column for color
                ),
            text=df_hospitals_filtered['name'],  # Hover text
            hoverinfo='text',
                hovertemplate=(
                "<b>Hospital:</b> %{text}<br>" +
                "<b>Number of beds:</b> %{marker.color}"
            ),
            showlegend=False,
            name=''
        )

        # Create the figure and add both layers
        fig.add_trace(layer)
        k += 1


    # Update the layout
    fig.update_layout(
        mapbox=dict(
            style=mapstyle,  # Map style
            center=dict(lat=51.2, lon=10.5),  # Center of the map
            zoom=5  # Initial zoom level
        ),
        width=600,  # Set width in pixels
        height=620,  # Set height in pixels
        margin=dict(l=0, r=0, t=0, b=0),  # Set margin to zero on all sides
    )

    return fig


def create_places_map(df_places, mapstyle, chart_colors):

    fig = go.Figure()
    # Create layer with places
    layer = go.Scattermapbox(
        lat=df_places['latitude'],
        lon=df_places['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=3,  # Scaled size of the markers
            color=df_places['zip'],  # Column for color scale
        ),
        text=df_places['name'],  # Hover text
        hoverinfo='text',
            hovertemplate=(
            "<b>Place:</b> %{text}<br>"
        ),
        showlegend=False,
        name=''
    )
    fig.add_trace(layer)

    # Update the layout
    fig.update_layout(
        mapbox=dict(
            style=mapstyle,  # Map style
            center=dict(lat=51.2, lon=10.5),  # Center of the map
            zoom=5  # Initial zoom level
        ),
        width=600,  # Set width in pixels
        height=620,  # Set height in pixels
        margin=dict(l=0, r=0, t=0, b=0),  # Set margin to zero on all sides
    )

    return fig


def map_css():
    return """
    <style>
    .stPlotlyChart {
        border-radius: 15px;  /* Set your desired border-radius here */
        overflow: hidden;      /* Ensure the border-radius is applied properly */
        margin: 0px 0px 0px 0px;            /* Remove padding */
    }
    </style>
    """


# Define function to establish connection to database
def establish_connection_to_database():
    load_dotenv()
    DB_PW = os.getenv('DB_PW')

    username = 'root'
    password = DB_PW
    host = 'localhost'
    port = '3306'
    database = 'hospital_register'

    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

    return engine


# CHARTS

def create_fig_nursing(engine, chart_colors):
    # Nursing quotient vs. total stations
    query = """
        SELECT hd.hospital_id, hd.nursing_quotient, hd.total_stations_count, hd.provider_type_code, pt.provider_type_name
        FROM hospital_details AS hd
        JOIN provider_types_dict AS pt ON hd.provider_type_code = pt.provider_type_code
        WHERE pt.language_code = 'en';
        """
    df_nursing = pd.read_sql(query, engine)

    # Create a horizontal violin plot
    fig_nursing = go.Figure()

    # Loop through each provider type and add a violin trace
    for provider_type in df_nursing['provider_type_code'].unique():
        fig_nursing.add_trace(go.Violin(
            x=df_nursing[df_nursing['provider_type_code'] == provider_type]['nursing_quotient'],
            y=df_nursing[df_nursing['provider_type_code'] == provider_type]['provider_type_name'],
            box_visible=True,
            line_color=chart_colors[provider_type],
            name=provider_type,
            fillcolor=chart_colors[provider_type],
            hoverinfo='x',  # Display x values on hover
            orientation='h'  # Make the violin plot horizontal
        ))

    # Update the layout
    fig_nursing.update_layout(
        xaxis_title='',
        yaxis_title='',
        title={'text': 'Patient to Nursing Staff Ratio', 'x': 0.55, 'xanchor': 'center', 'y': 0.95},
        showlegend=False,
        height=500,
        xaxis_range=[10, 90]
    )

    return fig_nursing


def create_fig_hospital_numbers(engine, chart_colors):
    # Number of Hospitals per Provider Type
    query = """
    SELECT pt.provider_type_name, pt.provider_type_code, COUNT(hd.hospital_id) AS num_hospitals
    FROM hospital_details hd
    INNER JOIN provider_types_dict pt ON hd.provider_type_code = pt.provider_type_code
    WHERE pt.language_code = 'en'
    GROUP BY pt.provider_type_name, pt.provider_type_code;
    """
    df_hospitals = pd.read_sql(query, engine)
    fig = px.bar(df_hospitals, x='provider_type_name', y='num_hospitals', color='provider_type_code', 
                color_discrete_map=chart_colors)
    fig.update_layout(xaxis_title='', yaxis_title='', showlegend=False,
                       title={'text': 'Number of Hospitals', 'x': 0.6, 'xanchor': 'center'})
    
    return fig


def create_fig_treatment_numbers(engine, chart_colors):
    # Number of Treatments per Provider Type
    query = """
    SELECT pt.provider_type_name, pt.provider_type_code, SUM(ht.treatment_count) AS num_treatments
    FROM hospital_treatments ht
    INNER JOIN hospital_details hd ON ht.hospital_id = hd.hospital_id
    INNER JOIN provider_types_dict pt ON hd.provider_type_code = pt.provider_type_code
    WHERE pt.language_code = 'en'
    GROUP BY pt.provider_type_name, pt.provider_type_code;
    """
    df_treatments = pd.read_sql(query, engine)
    fig = px.bar(df_treatments, x='provider_type_name', y='num_treatments', color='provider_type_code', 
                color_discrete_map=chart_colors)
    fig.update_layout(xaxis_title='', yaxis_title='', showlegend=False,
                       title={'text': 'Number of Treatments', 'x': 0.6, 'xanchor': 'center'})
    
    return fig


def create_fig_emergency(engine, chart_colors):
    # Distribution of Hospitals with Emergency Services by Provider Type
    query5 = """
    SELECT pt.provider_type_name, pt.provider_type_code, hd.has_emergency_service, COUNT(hd.hospital_id) AS num_hospitals
    FROM hospital_details hd
    INNER JOIN provider_types_dict pt ON hd.provider_type_code = pt.provider_type_code
    WHERE pt.language_code = 'en'
    GROUP BY pt.provider_type_name, pt.provider_type_code, hd.has_emergency_service;
    """

    df_emergency = pd.read_sql(query5, engine)

    # Calculate percentage for stacked percentage bar chart
    df_emergency_total = df_emergency.groupby(['provider_type_name', 'provider_type_code'])['num_hospitals'].sum().reset_index(name='total_hospitals')
    df_emergency = df_emergency.merge(df_emergency_total, on=['provider_type_name', 'provider_type_code'])
    df_emergency['percentage'] = df_emergency['num_hospitals'] / df_emergency['total_hospitals'] * 100

    # Fix: Apply the correct color based on provider type and emergency service status
    def get_color(row):
        base_color = chart_colors[row['provider_type_code']]
        opacity = 1 if row['has_emergency_service'] else 0.2
        r, g, b = tuple(int(base_color[i:i+2], 16) for i in (1, 3, 5))
        return f'rgba({r}, {g}, {b}, {opacity})'

    df_emergency['color'] = df_emergency.apply(get_color, axis=1)

    fig = go.Figure()

    # Add bars for each provider type with appropriate color
    for provider_type in df_emergency['provider_type_code'].unique():
        provider_data = df_emergency[df_emergency['provider_type_code'] == provider_type]
        fig.add_trace(go.Bar(
            x=provider_data['percentage'],
            y=provider_data['provider_type_name'],
            orientation='h',
            text=provider_data.apply(lambda row: f'{row["percentage"]:.0f}%' if row['has_emergency_service'] else '', axis=1),
            textposition='inside',  # Place the text inside the bar
            texttemplate='%{text}', # Ensures the text is formatted as expected
            marker_color=provider_data['color'],
            name=provider_type
        ))

    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        barmode='stack',
        showlegend=False,
        title={
            'text': 'Hospitals with Emergency Service',
            'x': 0.55,
            'y': 0.95,
            'xanchor': 'center'
        },
        bargap=0.2,  # Adjust the gap between bars
        height=250,  # Adjust the height as needed
    )
    fig.update_xaxes(visible=False)

    return fig



def create_fig_size_distribution(engine, chart_colors):
    # Hospital size distribution per Provider Type
    query = """
        SELECT hd.hospital_id, hd.bed_count, hd.provider_type_code, pt.provider_type_name
        FROM hospital_details AS hd
        INNER JOIN provider_types_dict AS pt ON hd.provider_type_code = pt.provider_type_code
        WHERE pt.language_code = 'en';
        """
    engine = establish_connection_to_database()
    df_hospital_size = pd.read_sql(query, engine)

    # Create a horizontal violin plot
    fig_hospital_size = go.Figure()

    # Loop through each provider type and add a violin trace
    for provider_type in df_hospital_size['provider_type_code'].unique():
        fig_hospital_size.add_trace(go.Violin(
            x=df_hospital_size[df_hospital_size['provider_type_code'] == provider_type]['bed_count'],
            y=df_hospital_size[df_hospital_size['provider_type_code'] == provider_type]['provider_type_name'],
            box_visible=True,
            line_color=chart_colors[provider_type],
            name=provider_type,
            fillcolor=chart_colors[provider_type],
            hoverinfo='x',  # Display x values on hover
            orientation='h'  # Make the violin plot horizontal
        ))

    # Update the layout
    fig_hospital_size.update_layout(
        xaxis_title='Number of Beds',
        yaxis_title='',
        title={'text': 'Distribution of Hospital Sizes', 'x': 0.5, 'xanchor': 'center', 'y': 0.95},
        showlegend=False,
        height=500,
    )

    return fig_hospital_size


def create_fig_beds_per_capita_states(engine, chart_colors):
    query = """
    SELECT hl.federal_state_code, fsd.federal_state_name, hd.provider_type_code, SUM(hd.bed_count)/fs.population*1000 AS beds_per_1000_capita
        FROM hospital_details AS hd
        INNER JOIN hospital_locations AS hl ON hl.hospital_id = hd.hospital_id
        INNER JOIN federal_states AS fs ON fs.federal_state_code = hl.federal_state_code
        INNER JOIN federal_states_dict AS fsd ON fsd.federal_state_code = fs.federal_state_code
        WHERE fsd.language_code = 'en'
        GROUP BY hl.federal_state_code, fsd.federal_state_name, hd.provider_type_code;
    """
    df_beds_per_1000_capita = pd.read_sql(query, engine)

    # Calculate the total bed count for each federal state
    df_total = df_beds_per_1000_capita.groupby('federal_state_name').agg({'beds_per_1000_capita': 'sum'}).reset_index()

    # Merge the total bed count with the original dataframe
    df_beds_per_1000_capita = pd.merge(df_beds_per_1000_capita, df_total, on='federal_state_name', suffixes=('', '_total'))

    # Sort the dataframe by total bed count
    df_beds_per_1000_capita = df_beds_per_1000_capita.sort_values(by='beds_per_1000_capita_total', ascending=True)
    df_total['beds_per_1000_capita'] = df_total['beds_per_1000_capita'].round(1)

    # Create the Plotly figure
    fig = go.Figure()

    # Add traces for each provider type
    for provider_type in df_beds_per_1000_capita['provider_type_code'].unique():
        provider_data = df_beds_per_1000_capita[df_beds_per_1000_capita['provider_type_code'] == provider_type]
        fig.add_trace(go.Bar(
            y=provider_data['federal_state_name'],  # y-axis as federal states
            x=provider_data['beds_per_1000_capita'],       # x-axis as sum of bed count
            orientation='h',                        # horizontal bars
            name=provider_type,                     # name of the trace
            marker_color=chart_colors[provider_type], # Use the colors from chart_colors dictionary
            #text=provider_data['beds_per_1000_capita'],    # Add the beds_per_1000_capita as text inside the bars
            #textposition='inside',                  # Position the text inside the bars
        ))

    # Add annotations for the total bed count next to each bar
    annotations = []
    for index, row in df_total.iterrows():
        annotations.append(dict(
            x=row['beds_per_1000_capita'],
            y=row['federal_state_name'],
            text=f"{row['beds_per_1000_capita']}",
            xanchor='left',
            yanchor='middle',
            showarrow=False,
            font=dict(size=12)
        ))

    # Update layout
    fig.update_layout(
        title={'text': 'Hospital Beds per 1000 Capita', 'x': 0.5, 'xanchor': 'center', 'y':0.95},
        xaxis_title='',
        yaxis_title='',
        barmode='stack',  # Stack the bars
        showlegend=False,  # Show the legend
        height=600,       # Adjust height as needed
        annotations=annotations  # Add the annotations to the layout
    )

    fig.update_xaxes(visible=False)

    return fig