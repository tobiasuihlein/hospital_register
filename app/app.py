import pandas as pd
import streamlit as st
import plotly.express as px
from app_functions import *
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
import streamlit.components.v1 as components


cont = {
    'en': {
        'menu_home': 'Home',
        'menu_hospital_map': 'Hospital Map',
        'menu_places_map': 'Places Map',
        'hospital_map_title': 'Distribution of Hospitals',
        'places_map_title': 'Places in Germany',
        'size': 'Size',
        'provider_type': 'Provider Type',
        'public': 'Public',
        'private': 'Private',
        'non_profit': 'Non-profit'
    },
    'de': {
        'hospital_map_title': 'Krankenhäuser in Deutschland',
        'size': 'Größe',
        'provider_type': 'Träger',
        'public': 'Öffentlich',
        'private': 'Privat',
        'non_profit': 'Gemeinnützig'
    }
}


chart_colors = {
    'O': '#636EFA', # public
    'P': '#00CC96', # private
    'F': '#FFA15A' # non-profit
}

lang = 'en'


css_remove_whitespace_from_top_of_the_page = '''
<style>
    .block-container {
        padding-top: 5rem;
        padding-bottom: 5rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
</style>
'''

ms = st.session_state

st.markdown(css_remove_whitespace_from_top_of_the_page, unsafe_allow_html=True)


# set theme
if "themes" not in ms: 
    ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    "light": {"theme.base": "dark",
                              "theme.primaryColor": "#adadb2"},
                    "dark":  {"theme.base": "light",
                              "theme.primaryColor": "#223349"}
                    }

def ChangeTheme():
    previous_theme = ms.themes["current_theme"]
    tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
    for vkey, vval in tdict.items(): 
        if vkey.startswith("theme"): st._config.set_option(vkey, vval)
    ms.themes["refreshed"] = False
    if previous_theme == "dark":
        ms.themes["current_theme"] = "light"
        ms.mapstyle = 'open-street-map'
    elif previous_theme == "light":
        ms.themes["current_theme"] = "dark"
        ms.mapstyle = 'carto-darkmatter'

# dark mode toggle
st.sidebar.toggle("Dark Mode", False, on_change=ChangeTheme)
if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()


# MENU BAR

# Create a menu to navigate between the pages
selected = option_menu(
menu_title=None,
options = ['Overview', 'Lab', cont[lang]['menu_hospital_map'], cont[lang]['menu_places_map']],
icons = ["house", "lab", "map", "map"],
menu_icon = "cast",
orientation = "horizontal")


# OVERVIEW PAGE
if selected == 'Overview':

    # Get Data and create charts

    engine = establish_connection_to_database()

    # Number of Hospitals per Provider Type
    query1 = """
    SELECT pt.provider_type_name, pt.provider_type_code, COUNT(hd.hospital_id) AS num_hospitals
    FROM hospital_details hd
    INNER JOIN provider_types_dict pt ON hd.provider_type_code = pt.provider_type_code
    WHERE pt.language_code = 'en'
    GROUP BY pt.provider_type_name, pt.provider_type_code;
    """
    df_hospitals = pd.read_sql(query1, engine)
    fig1 = px.bar(df_hospitals, x='provider_type_name', y='num_hospitals', color='provider_type_code', 
                color_discrete_map=chart_colors)
    fig1.update_layout(xaxis_title='', yaxis_title='', showlegend=False,
                       title={'text': 'Number of Hospitals', 'x': 0.6, 'xanchor': 'center'})
    

    # Number of Treatments per Provider Type
    query2 = """
    SELECT pt.provider_type_name, pt.provider_type_code, SUM(ht.treatment_count) AS num_treatments
    FROM hospital_treatments ht
    INNER JOIN hospital_details hd ON ht.hospital_id = hd.hospital_id
    INNER JOIN provider_types_dict pt ON hd.provider_type_code = pt.provider_type_code
    WHERE pt.language_code = 'en'
    GROUP BY pt.provider_type_name, pt.provider_type_code;
    """
    df_treatments = pd.read_sql(query2, engine)
    fig2 = px.bar(df_treatments, x='provider_type_name', y='num_treatments', color='provider_type_code', 
                color_discrete_map=chart_colors)
    fig2.update_layout(xaxis_title='', yaxis_title='', showlegend=False,
                       title={'text': 'Number of Treatments', 'x': 0.6, 'xanchor': 'center'})

    
    # Hospital size distribution per Provider Type
    query = """
        SELECT hd.hospital_id, hd.bed_count, hd.provider_type_code, pt.provider_type_name
        FROM hospital_details AS hd
        INNER JOIN provider_types_dict AS pt ON hd.provider_type_code = pt.provider_type_code
        WHERE pt.language_code = 'en';
        """
    engine = establish_connection_to_database()
    df_hospital_size = pd.read_sql(query, engine)
    
    colors_hospital_size = [chart_colors[provider_type] for provider_type in df_hospital_size['provider_type_code']]

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


    # 5. Distribution of Hospitals with Emergency Services by Provider Type
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
        opacity = 1 if row['has_emergency_service'] else 0.5
        r, g, b = tuple(int(base_color[i:i+2], 16) for i in (1, 3, 5))
        return f'rgba({r}, {g}, {b}, {opacity})'

    df_emergency['color'] = df_emergency.apply(get_color, axis=1)

    fig5 = go.Figure()

    # Add bars for each provider type with appropriate color
    for provider_type in df_emergency['provider_type_code'].unique():
        provider_data = df_emergency[df_emergency['provider_type_code'] == provider_type]
        fig5.add_trace(go.Bar(
            x=provider_data['percentage'],
            y=provider_data['provider_type_name'],
            orientation='h',
            text=provider_data.apply(lambda row: f'{row["percentage"]:.0f}%' if row['has_emergency_service'] else '', axis=1),
            textposition='inside',  # Place the text inside the bar
            texttemplate='%{text}', # Ensures the text is formatted as expected
            marker_color=provider_data['color'],
            name=provider_type
        ))

    fig5.update_layout(
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
        bargap=0.4,  # Adjust the gap between bars
    )


    # 6. Average Number of Treatments for Different Treatment Names by Provider Type
    query6 = """
    SELECT td.treatment_name, pt.provider_type_name, pt.provider_type_code, AVG(ht.treatment_count) AS avg_treatment_count
    FROM hospital_treatments ht
    INNER JOIN treatments_dict td ON ht.treatment_code = td.treatment_code
    INNER JOIN hospital_details hd ON ht.hospital_id = hd.hospital_id
    INNER JOIN provider_types_dict pt ON hd.provider_type_code = pt.provider_type_code
    WHERE td.language_code = 'en' AND pt.language_code = 'en'
    GROUP BY td.treatment_name, pt.provider_type_name, pt.provider_type_code;
    """
    df_avg_treatments_names = pd.read_sql(query6, engine)
    fig6 = px.bar(df_avg_treatments_names, x='avg_treatment_count', y='treatment_name', color='provider_type_code', 
                color_discrete_map=chart_colors, barmode='group', orientation='h')
    fig6.update_layout(title='Average Number of Treatments for Different Treatment Names by Provider Type', 
                    xaxis_title='Average Treatment Count', yaxis_title='', showlegend=False, height=1200)


    # Text and Chart Display

    st.markdown("""
                <h4>Introduction</h4>
                <p>
                In Germany exist three different types of hospitals: public, private and non-profit.
                The following analysis provides an overview of various hospital characteristics by provider type.
                </p>
                """, unsafe_allow_html=True)
    
    st.markdown("""
            <h4>Number of hospitals and treatments</h4>
            <p>
            Regarding the total number of hospitals of the different types, non-profit and public are the most common, while to number of private hospitals is about 20 percent lower.
            The total number of treatments is higher for public than for non-profit hospitals, private hospitals have the lowest total number of treatments.
            </p>
            """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            fig1.update_layout(margin=dict(l=20, r=20, t=60, b=0))
            st.plotly_chart(fig1)
        with col2:
            fig2.update_layout(margin=dict(l=20, r=20, t=60, b=0))
            st.plotly_chart(fig2)

    st.markdown("""
        <h4>Hospital Size</h4>
        <p>
        The differences in number of hospitals and treatments ralate to the distribution of hospital sizes: private hospitals tend to be smaller, while public and non-profit hospitals are larger.
        The largest hospitals with more than 1000 beds are mostly public hospitals.
        </p>
        """, unsafe_allow_html=True)

    fig_hospital_size.update_layout(margin=dict(l=20, r=20, t=60, b=0))
    st.plotly_chart(fig_hospital_size, use_container_width=True)

    st.markdown("""
        <h4>Emergency Services</h4>
        <p>The availability of emergency service is very different between the provider types.
        While most of the public hospitals have emergency services, only about half of private hospitals offer this service. Non-profit hospitals are in between with a rate of three out of four.
        </p>
        """, unsafe_allow_html=True)

    fig5.update_layout(margin=dict(l=20, r=20, t=40, b=0))
    st.plotly_chart(fig5)

    st.plotly_chart(fig6)

# HOME PAGE
if selected == 'Lab':


    st.markdown(f"<h2 style='text-align: center; padding: 10'>Data Analysis</h2>", unsafe_allow_html=True)           
    st.markdown(f"""
                <p style='text-align: center; padding: 10'>
                    <span style='color: {chart_colors['O']}'>⬤</span> {cont[lang]['public']}
                    <span style='color: {chart_colors['P']}'>&nbsp;&nbsp;⬤</span> {cont[lang]['private']}
                    <span style='color: {chart_colors['F']}'>&nbsp;&nbsp;⬤</span> {cont[lang]['non_profit']}
                </p>
                """, unsafe_allow_html=True)


    # Hospital treatments

    # Bar chart for treatments


    # Assuming you have already established a database connection and fetched the data into df_barchart
    query = """
    SELECT ht.treatment_code, hd.provider_type_code, td.treatment_name, 
        SUM(ht.treatment_count) sum_treatment_count, 
        SUM(hd.total_treatments) AS sum_total_treatments, 
        AVG(ht.treatment_count/total_treatments*100) AS avg_treatment_count_share
        FROM hospital_treatments AS ht
        INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
        INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
        WHERE td.language_code = 'en' AND ht.treatment_count > 0
        GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
    """
    engine = establish_connection_to_database()
    df_barchart = pd.read_sql(query, engine)

    # Sort by sum_total_treatments
    df_barchart = df_barchart.sort_values(by='sum_total_treatments', ascending=False)

    # Create the horizontal bar chart
    fig_barchart = px.bar(
        df_barchart,
        x='avg_treatment_count_share', 
        y='treatment_name', 
        color='provider_type_code',
        color_discrete_map=chart_colors,
        orientation='h',
        labels={
            'avg_treatment_count_share': 'Average Treatment Count Share (%)',
            'treatment_name': 'Treatment Name'
        },
        height=800,  # Adjust the height as needed
    )

    # Update layout to better organize the plot
    fig_barchart.update_layout(
        title={'text': 'Average Treatment Count Share by Treatment and Provider Type', 'x': 0.5, 'xanchor': 'center'},
        xaxis_title='Average Treatment Count Share (%)',
        yaxis_title='',
        barmode='group',  # Group bars together by treatment_name
        showlegend=False,
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig_barchart, use_container_width=True)



    # New bubble chart

    # Assuming you have already established a database connection and fetched the data into df_bubble_chart
    query = """
    SELECT ht.treatment_code, hd.provider_type_code, td.treatment_name, COUNT(ht.hospital_id) AS hospital_count, SUM(ht.treatment_count) sum_treatment_count, 
        SUM(hd.total_treatments) AS sum_total_treatments, 
        AVG(ht.treatment_count/total_treatments*100) AS avg_treatment_count_share
        FROM hospital_treatments AS ht
        INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
        INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
        WHERE td.language_code = 'en' AND ht.treatment_count > 0
        GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
    """
    engine = establish_connection_to_database()
    df_bubble_chart = pd.read_sql(query, engine)

    # Sort by sum_total_treatments
    df_bubble_chart = df_bubble_chart.sort_values(by='sum_total_treatments', ascending=False)

    # Create the bubble chart
    fig_bubble_chart = px.scatter(
        df_bubble_chart, 
        x='avg_treatment_count_share', 
        y='treatment_name', 
        size='hospital_count',  # Size of bubbles
        color='provider_type_code',
        color_discrete_map=chart_colors,
        hover_name='treatment_name',
        hover_data={'sum_treatment_count': True, 'avg_treatment_count_share': True, 'sum_total_treatments': True},
        size_max=20,  # Max bubble size
        height=800,  # Adjust height as needed
        labels={
            'sum_treatment_count': 'Sum of Treatment Count',
            'treatment_name': 'Treatment Name',
            'avg_treatment_count_share': 'Average Treatment Count Share (%)'
        }
    )


    # Update the layout
    fig_bubble_chart.update_layout(
        title={'text': 'Bubble Chart of Treatment Distribution by Provider Type', 'x': 0.5, 'xanchor': 'center'},
        xaxis_title='Sum of Treatment Count',
        yaxis_title='',
        yaxis=dict(categoryorder='total ascending'),  # Order treatments by total sum_treatment_count
        showlegend=False,
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig_bubble_chart, use_container_width=True)


    # Violin plot
    query = f"""
        WITH total_count_per_treatment AS
            (SELECT ht.treatment_code, SUM(ht.treatment_count) AS sum_treatment_count, AVG(ht.treatment_count) AS avg_treatment_count
                FROM hospital_treatments AS ht
                GROUP BY ht.treatment_code)
        SELECT ht.treatment_code, td.treatment_name, hd.provider_type_code, ht.treatment_count, tcpt.sum_treatment_count, tcpt.avg_treatment_count, (ht.treatment_count-tcpt.avg_treatment_count)/tcpt.avg_treatment_count AS relative_treatment_count
            FROM hospital_treatments AS ht
            INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
            INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
            INNER JOIN total_count_per_treatment AS tcpt ON tcpt.treatment_code = ht.treatment_code
            WHERE td.language_code = 'en' AND ht.treatment_count > 0;
        """
    engine = establish_connection_to_database()
    df_treatments = pd.read_sql(query, engine)

    # Create a horizontal violin plot
    fig_treatments = go.Figure()

    # Loop through each provider type and add a violin trace for each treatment
    for provider_type in df_treatments['provider_type_code'].unique():
        for treatment_name in df_treatments['treatment_name'].unique():
            filtered_data = df_treatments[
                (df_treatments['provider_type_code'] == provider_type) & 
                (df_treatments['treatment_name'] == treatment_name)
            ]
            fig_treatments.add_trace(go.Violin(
                x=filtered_data['relative_treatment_count'],
                y=[treatment_name] * len(filtered_data),  # Repeat the treatment_name for y-axis
                line_color=chart_colors[provider_type],
                name=f"{treatment_name} ({provider_type})",
                fillcolor=chart_colors[provider_type],
                hoverinfo='x',
                opacity=0.6,  # Adjust the opacity as needed
                orientation='h',
            ))

    # Update layout for the figure
    fig_treatments.update_layout(
        xaxis_title='Relative Treatment Count',
        yaxis_title='Treatment Name',
        title={'text': 'Distribution of Relative Treatment Counts by Treatment and Provider Type', 'x': 0.5, 'xanchor': 'center'},
        showlegend=False,  # You can set this to True if you want a legend
        height=3000,  # Adjust height as needed to fit all treatments
        xaxis=dict(
            title='Relative Treatment Count',
            range=[-5, 50]  # Ensure x-axis has a bit of extra space
        ),
        yaxis=dict(
            title='Treatment Name',
            categoryorder='total ascending',  # Order treatments based on total
        )
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig_treatments, use_container_width=True)


    # Bar chart
    query = f"""
        SELECT ht.treatment_code, td.treatment_name, hd.provider_type_code, AVG(ht.treatment_count) AS avg_treatment_count, COUNT(ht.hospital_id) AS hospital_count, AVG(hd.bed_count) AS avg_bed_count
        FROM hospital_treatments AS ht
        INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
        INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
        WHERE td.language_code = 'en' AND ht.treatment_count > 0
        GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
        """
    engine = establish_connection_to_database()
    df_treatments = pd.read_sql(query, engine)
    df_treatments = df_treatments.sort_values(by=['avg_treatment_count'], ascending=True) 

    colors_treatments = [chart_colors[provider_type] for provider_type in df_treatments['provider_type_code']]

    fig_treatments = px.bar(
        df_treatments, x='hospital_count', y='treatment_name', color='provider_type_code', color_discrete_map=chart_colors,
        orientation='h'
    )
    fig_treatments.update_layout(
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        title={'text': 'Number of hospitals providing specific treatments', 'x': 0.5, 'xanchor': 'center',},
        showlegend=False,
        height=800,
    )
    st.plotly_chart(fig_treatments, use_container_width=True)



    # Bubble chart

    # SQL query and data fetching (assuming function and connection are already defined)
    query = """
        SELECT ht.treatment_code, td.treatment_name, hd.provider_type_code, AVG(ht.treatment_count) AS avg_treatment_count, SUM(ht.treatment_count) AS sum_treatment_count, COUNT(ht.hospital_id) AS hospital_count, AVG(hd.bed_count) AS avg_bed_count
        FROM hospital_treatments AS ht
        INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
        INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
        WHERE td.language_code = 'en' AND ht.treatment_count > 0
        GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
    """
    engine = establish_connection_to_database()
    df_treatments = pd.read_sql(query, engine)

    # Sort data by average treatment count if needed
    # Aggregate data to calculate the total hospital count per treatment across all provider types
    df_aggregated = df_treatments.groupby('treatment_code').agg(
        total_hospital_count=('hospital_count', 'sum'),
        total_treatment_count=('sum_treatment_count', 'sum')
    ).reset_index()

    # Merge the aggregated data back with the original data to maintain details for plotting
    df_treatments_merged = pd.merge(df_treatments, df_aggregated, on='treatment_code', suffixes=('', '_total'))

    # Sort data by the aggregated total hospital count
    df_treatments_sorted = df_treatments_merged.sort_values(by='total_treatment_count', ascending=True)

    colors_treatments = [chart_colors[provider_type] for provider_type in df_treatments_sorted['provider_type_code']]

    fig_treatments = px.scatter(
        df_treatments_sorted, 
        x='hospital_count', 
        y='treatment_name', 
        size='sum_treatment_count',  # Size of bubbles
        color='provider_type_code', 
        color_discrete_map=chart_colors,
        title='Number of Hospitals Providing Specific Treatments',
        labels={'hospital_count': 'Number of Hospitals', 'avg_treatment_count': 'Average Treatment Count'}
    )

    # Update layout for better visualization
    fig_treatments.update_layout(
        xaxis_title='',
        yaxis_title='',
        title={'text': 'Number of Hospitals Providing Specific Treatments', 'x': 0.5, 'xanchor': 'center'},
        showlegend=False,  # Show legend to differentiate provider types
        height=800
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig_treatments, use_container_width=True)


    # Nursing quotient vs. total stations
    query = """
        SELECT hd.hospital_id, hd.nursing_quotient, hd.total_stations_count, hd.provider_type_code
	    FROM hospital_details AS hd;
        """
    engine = establish_connection_to_database()
    df_nursing = pd.read_sql(query, engine)

    colors_nursing = [chart_colors[provider_type] for provider_type in df_nursing['provider_type_code']]
    
    fig_nursing = go.Figure(data=go.Scatter(
        x=df_nursing['total_stations_count'], y=df_nursing['nursing_quotient'],
        mode='markers', marker=dict(color=colors_nursing),
        )
    )
    fig_nursing.update_layout(
        xaxis_title='Total Stations',
        yaxis_title='Nursing Quotient',
        title={'text': 'Nursing Quotient vs. Total Stations in Hospitals', 'x': 0.55, 'xanchor': 'center', 'y': 0.85},
        showlegend=False
    )
    st.plotly_chart(fig_nursing, use_container_width=True)



    # Nursing staff vs. total stations
    query = """
        SELECT hd.hospital_id, hd.nursing_count, hd.total_stations_count, hd.provider_type_code
	    FROM hospital_details AS hd;
        """
    engine = establish_connection_to_database()
    df_nursing = pd.read_sql(query, engine)

    colors_nursing = [chart_colors[provider_type] for provider_type in df_nursing['provider_type_code']]
    
    fig_nursing = go.Figure(data=go.Scatter(
        x=df_nursing['total_stations_count'], y=df_nursing['nursing_count'],
        mode='markers', marker=dict(color=colors_nursing),
        )
    )
    fig_nursing.update_layout(
        xaxis_title='Total Stations',
        yaxis_title='Nursing Staff Count',
        title={'text': 'Nursing Staff Count vs. Total Stations in Hospitals', 'x': 0.55, 'xanchor': 'center', 'y': 0.85},
        showlegend=False
    )
    st.plotly_chart(fig_nursing, use_container_width=True)





# HOSPITAL MAP PAGE
if selected == cont[lang]['menu_hospital_map']:

    # sidebar with filter options
    with st.sidebar:

        # Sidebar header
        st.markdown("<h2>Filter Options</h2>", unsafe_allow_html=True)

        st.markdown("<h4>Size</h4>", unsafe_allow_html=True)
        # Define slider for minimum and maximum number of hospital beds
        min_hospital_beds = st.slider('Minimum number of beds', min_value=0, max_value=1500, value=0, label_visibility='visible')
        max_hospital_beds = st.slider('Maximum number of beds', min_value=0, max_value=1500, value=1500, label_visibility='visible')

        # Define checkboxes for provider types
        provider_type_labels = [cont[lang]['public'], cont[lang]['private'], cont[lang]['non_profit']]
        provider_types = []
        st.markdown("<h4>Provider Type</h4>", unsafe_allow_html=True)
        provider_type_O = st.checkbox(provider_type_labels[0], value=True)
        if provider_type_O:
            provider_types.append('O')
        provider_type_P = st.checkbox(provider_type_labels[1], value=True)
        if provider_type_P:
            provider_types.append('P')
        provider_type_F = st.checkbox(provider_type_labels[2], value=True)
        if provider_type_F:
            provider_types.append('F')

    # Get hospitals data
    if len(provider_types) != 0 and min_hospital_beds < max_hospital_beds:
        query = f"""
            SELECT name, hd.provider_type_code, hd.bed_count AS beds_number, latitude, longitude
            FROM hospital_locations AS hl
            JOIN hospital_details AS hd ON hl.hospital_id = hd.hospital_id
            WHERE hd.bed_count >= {min_hospital_beds}
            AND hd.bed_count <= {max_hospital_beds}
            AND hd.provider_type_code IN {query_tuple(provider_types)}
            """
        engine = establish_connection_to_database()
        df_hospitals = pd.read_sql(query, engine)
    else:
        # dummy data for empty map
        df_hospitals = pd.DataFrame({'name': ['dummy_1', 'dummy_2'], 'provider_type_code': ['O', 'O'], 'beds_number': [1, 2], 'latitude': [0.0, 0.0], 'longitude': [0.0, 0.0]})

    # Create figures        
    if "mapstyle" not in ms:
        mapstyle = 'open-street-map'
    else:
        mapstyle = ms.mapstyle

    fig_hospitals = create_hospital_map_new(df_hospitals, mapstyle, chart_colors)
    

    with st.container():
        col1, col2, col3 = st.columns([1, 10, 1])

        with col2:
            # Render figures
            st.markdown(map_css(), unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; padding: 10'>{cont[lang]['hospital_map_title']}</h2>", unsafe_allow_html=True)
            st.markdown(f"""
                        <p style='text-align: center; padding: 10'>
                            <span style='color: {chart_colors['O']}'>⬤</span> {cont[lang]['public']}
                            <span style='color: {chart_colors['P']}'>&nbsp;&nbsp;⬤</span> {cont[lang]['private']}
                            <span style='color: {chart_colors['F']}'>&nbsp;&nbsp;⬤</span> {cont[lang]['non_profit']}
                        </p>
                        """, unsafe_allow_html=True)
            st.plotly_chart(fig_hospitals, use_container_width=True)


# PLACES MAP PAGE
elif selected == cont[lang]['menu_places_map']:

    # Get places data
    query = """
        SELECT name, latitude, longitude, zip
        FROM places
        """
    engine = establish_connection_to_database()
    df_places = pd.read_sql(query, engine)
    df_places['zip'] = df_places['zip'].astype(int)

    # Create figures        
    if "mapstyle" not in ms:
        mapstyle = 'open-street-map'
    else:
        mapstyle = ms.mapstyle

    fig_places = create_places_map(df_places, mapstyle, chart_colors)

    with st.container():
        col1, col2, col3 = st.columns([1, 10, 1])

        with col2:
            # Render figures
            st.markdown(map_css(), unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; padding: 10'>{cont[lang]['places_map_title']}</h2>", unsafe_allow_html=True)
            st.plotly_chart(fig_places, use_container_width=True)