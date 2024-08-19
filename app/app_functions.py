import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


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