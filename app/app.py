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
                    "light": {"theme.base": "dark",},
                    "dark":  {"theme.base": "light",},
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
options = ['Home', cont[lang]['menu_hospital_map'], cont[lang]['menu_places_map']],
icons = ["house", "map", "map"],
menu_icon = "cast",
orientation = "horizontal")


# HOME PAGE
if selected == 'Home':

    st.markdown(f"<h2 style='text-align: center; padding: 10'>Data Analysis</h2>", unsafe_allow_html=True)           
    st.markdown(f"""
                <p style='text-align: center; padding: 10'>
                    <span style='color: {chart_colors['O']}'>⬤</span> {cont[lang]['public']}
                    <span style='color: {chart_colors['P']}'>&nbsp;&nbsp;⬤</span> {cont[lang]['private']}
                    <span style='color: {chart_colors['F']}'>&nbsp;&nbsp;⬤</span> {cont[lang]['non_profit']}
                </p>
                """, unsafe_allow_html=True)


    # Hospital treatments
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

    # Create the bubble chart
    fig_treatments = px.scatter(
        df_treatments_sorted, 
        x='sum_treatment_count', 
        y='treatment_name', 
        size='avg_treatment_count',  # Size of bubbles
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


    # Hospital size distribution
    query = """
        SELECT hd.hospital_id, hd.bed_count, hd.provider_type_code
        FROM hospital_details AS hd;
        """
    engine = establish_connection_to_database()
    df_hospital_size = pd.read_sql(query, engine)
    
    colors_hospital_size = [chart_colors[provider_type] for provider_type in df_hospital_size['provider_type_code']]

    fig_hospital_size = go.Figure()

    # Loop through each provider type and add a histogram trace
    for provider_type in df_hospital_size['provider_type_code'].unique():
        fig_hospital_size.add_trace(go.Histogram(
            x=df_hospital_size[df_hospital_size['provider_type_code'] == provider_type]['bed_count'],
            marker_color=chart_colors[provider_type],
            hoverinfo='x+y',
            nbinsx=30,  # Number of bins
        ))

    # Update the layout to stack the histograms
    fig_hospital_size.update_layout(
        xaxis_title='Number of Beds',
        yaxis_title='Count',
        title={'text': 'Distribution of Hospital Sizes', 'x': 0.55, 'xanchor': 'center', 'y': 0.85},
        barmode='stack',  # Stack the bars
        showlegend=False
    )
    st.plotly_chart(fig_hospital_size, use_container_width=True)

    # Create a horizontal violin plot
    fig_hospital_size = go.Figure()

    # Loop through each provider type and add a violin trace
    for provider_type in df_hospital_size['provider_type_code'].unique():
        fig_hospital_size.add_trace(go.Violin(
            x=df_hospital_size[df_hospital_size['provider_type_code'] == provider_type]['bed_count'],
            y=df_hospital_size[df_hospital_size['provider_type_code'] == provider_type]['provider_type_code'],
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
        yaxis_title='Provider Type',
        title={'text': 'Distribution of Hospital Sizes by Provider Type', 'x': 0.5, 'xanchor': 'center'},
        showlegend=True,
        height=800
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig_hospital_size, use_container_width=True)


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