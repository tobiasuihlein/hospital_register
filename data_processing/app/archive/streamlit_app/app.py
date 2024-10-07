import pandas as pd
import streamlit as st
import plotly.express as px
from app_functions import *
from streamlit_option_menu import option_menu

# Define content for the app in different languages
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

# Define colors for the charts
chart_colors = {
    'O': '#636EFA', # public (blue)
    'P': '#00CC96', # private (green)
    'F': '#FFA15A', # non-profit (orange)
    'darkgray': '#7F7F7F',
    'lightgray': '#e0e0e0',
    'red': '#EF553B',
    'purple': '#AB63FA',
    'yellow': '#FECB52',
}

colorscales = ['Blugrn', 'Purp', 'Peach', 'Brwnyl']

# Define the language of the app
lang = 'en'

# Streamlit State
ms = st.session_state

# Add CSS for Layout
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
st.markdown(css_remove_whitespace_from_top_of_the_page, unsafe_allow_html=True)

# Set the theme (light and dark mode)
if "themes" not in ms: 
    ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    "light": {"theme.base": "dark",
                              "theme.primaryColor": "#adadb2"},
                    "dark":  {"theme.base": "light",
                              "theme.primaryColor": "#223349"}
                    }

# Define function to change the theme (light and dark mode)
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

# Dark mode toggle
st.sidebar.toggle("Dark Mode", False, on_change=ChangeTheme)
if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()


### MENU BAR ###

# Create a menu to navigate between the pages
selected = option_menu(
menu_title=None,
options = ['Overview', cont[lang]['menu_hospital_map']],
icons = ["house", "map"],
menu_icon = "cast",
orientation = "horizontal")


### OVERVIEW PAGE ###
if selected == 'Overview':

    # Get Data and create charts
    engine = establish_connection_to_database()
    fig_nursing = create_fig_nursing(engine, chart_colors)
    fig_hospital_numbers = create_fig_hospital_numbers(engine, chart_colors)
    fig_treatment_numbers = create_fig_treatment_numbers(engine, chart_colors)
    fig_emergency = create_fig_emergency(engine, chart_colors)
    fig_size_distribution = create_fig_size_distribution(engine, chart_colors)
    fig_beds_per_capita_states = create_fig_beds_per_capita_states(engine, chart_colors)


    ### Text and Chart Display ###

    # Introduction
    st.markdown(f"""
                <h4>Introduction</h4>
                <p>
                In Germany exist three different types of hospitals: <span style='color: {chart_colors['O']}'>⬤</span> {cont[lang]['public']}, <span style='color: {chart_colors['P']}'>⬤</span> {cont[lang]['private']} and <span style='color: {chart_colors['F']}'>⬤</span> {cont[lang]['non_profit']}.                
                The following analysis provides an overview of various hospital characteristics by provider type.
                </p>
                """, unsafe_allow_html=True)
    

    # Number of Hospitals and Treatments
    st.markdown("""
            <h4>Number of Hospitals and Treatments</h4>
            <p>
            Regarding the total number of hospitals of the different types, non-profit and public are the most common, while to number of private hospitals is about 20 percent lower.
            The total number of treatments is higher for public than for non-profit hospitals, private hospitals have the lowest total number of treatments.
            </p>
            """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            fig_hospital_numbers.update_layout(margin=dict(l=20, r=20, t=60, b=0))
            st.plotly_chart(fig_hospital_numbers)
        with col2:
            fig_treatment_numbers.update_layout(margin=dict(l=20, r=20, t=60, b=0))
            st.plotly_chart(fig_treatment_numbers)

    # Hospital Size
    st.markdown("""
        <h4>Hospital Size</h4>
        <p>
        The differences in number of hospitals and treatments ralate to the distribution of hospital sizes: private hospitals tend to be smaller, while public and non-profit hospitals are larger.
        The largest hospitals with more than 1000 beds are mostly public hospitals.
        </p>
        """, unsafe_allow_html=True)

    fig_size_distribution.update_layout(margin=dict(l=20, r=20, t=60, b=0))
    st.plotly_chart(fig_size_distribution, use_container_width=True)

    # Emergency Services
    st.markdown("""
        <h4>Emergency Services</h4>
        <p>The availability of emergency service is very different between the provider types.
        While most of the public hospitals have emergency services, only about half of private hospitals offer this service. Non-profit hospitals are in between with a rate of three out of four.
        </p>
        """, unsafe_allow_html=True)

    fig_emergency.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_emergency, use_container_width=True)

    # Nursing Staff
    st.markdown("""
        <h4>Nursing Staff</h4>
        <p>In general most hospitals have a patient to nursing staff ratio (nursing quotient) of 30 to 70.
        For public hospitals the variation of the nursing quotient is smaller than for the other provider types.
        The distribution of the nursing quotient of private hospitals is wider than for the other provider types, i.e there is a higher share of hospitals with relatively lower and higher nursing quotients.
        </p>
        """, unsafe_allow_html=True)  
    
    fig_nursing.update_layout(margin=dict(l=20, r=20, t=60, b=0))
    st.plotly_chart(fig_nursing, use_container_width=True)

    
    # Top Treatments
    st.markdown(f"""
                <h4>Top Treatments</h4>
                <p>The registered top treatmets for all provider types are Childbirth and Pneumonia.
                For private and non-profit hospitals knee and hip replacement are also among the top treatments, but not for public hospitals.
                <br><br>
                </p>
                """, unsafe_allow_html=True)
    
    query= """
    SELECT ht.treatment_code, hd.provider_type_code, td.treatment_name, SUM(ht.treatment_count) AS sum_treatment_count
	FROM hospital_treatments AS ht
    INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
    INNER JOIN treatments_dict as td ON td.treatment_code = ht.treatment_code
    WHERE td.language_code = 'en'
    GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
    """

    engine = establish_connection_to_database()

    df_top_treatments = pd.read_sql(query, engine)
    df_top_treatments_public = df_top_treatments.sort_values(by=['provider_type_code', 'sum_treatment_count'], ascending=True)
    df_top_treatments_public = df_top_treatments_public[df_top_treatments_public['provider_type_code'] == 'O'].tail(5)
    df_top_treatments_private = df_top_treatments.sort_values(by=['provider_type_code', 'sum_treatment_count'], ascending=True)
    df_top_treatments_private = df_top_treatments_private[df_top_treatments_private['provider_type_code'] == 'P'].tail(5)
    df_top_treatments_non_profit = df_top_treatments.sort_values(by=['provider_type_code', 'sum_treatment_count'], ascending=True)
    df_top_treatments_non_profit = df_top_treatments_non_profit[df_top_treatments_non_profit['provider_type_code'] == 'F'].tail(5)
    
    fig_list = []
    for df in [df_top_treatments_public, df_top_treatments_private, df_top_treatments_non_profit]:
        fig = go.Figure()
        fig = px.bar(df, x='sum_treatment_count', y='treatment_name', color='provider_type_code', color_discrete_map=chart_colors, orientation='h', height=150)
        fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        title={'text': '', 'x': 0.5, 'xanchor': 'center'},
        showlegend=False,
        margin=dict(l=20, r=20, t=0, b=0)
    )
        fig_list.append(fig)

    for fig in fig_list:
       st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
        <p style='text-align: center; padding: 0px 0 20px 0'>
            <span style='color: {chart_colors['O']}'>⬤</span> {cont[lang]['public']}
            <span style='color: {chart_colors['P']}'>&nbsp;&nbsp;&nbsp;&nbsp;⬤</span> {cont[lang]['private']}
            <span style='color: {chart_colors['F']}'>&nbsp;&nbsp;&nbsp;&nbsp;⬤</span> {cont[lang]['non_profit']}
        </p>
        """, unsafe_allow_html=True)

    # Beds per Capita
    st.markdown("""
        <h4>Beds per Capita</h4>
        <p>
        The number of beds per capita varies between the states.
        The states with the highest number of beds per capita are Thuringia, Saarland, Bremen and Hamburg with 5.6 to 5.8 beds per 1000 inhabitants.
        Baden-Württemberg as the state with the lowest number of beds per capita has 3.6 beds per 1000 inhabitants.
        In the different states also different provider types are more common.
        While Saarland, for example has no private hospitals, in Hamburg the share of private hospitals is the highest among the provider types.
        </p>
        """, unsafe_allow_html=True)

    fig_beds_per_capita_states.update_layout(margin=dict(l=20, r=20, t=60, b=0))
    st.plotly_chart(fig_beds_per_capita_states, use_container_width=True)



### HOSPITAL MAP PAGE ###
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
    
    # Set layout for map display
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