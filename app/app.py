import pandas as pd
import streamlit as st
import plotly.express as px
from app_functions import *
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
import streamlit.components.v1 as components


cont = {
    'en': {
        'hospital_map_title': 'Hospitals in Germany',
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

lang = 'en'

st.set_page_config(layout="wide")

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


ms = st.session_state


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

st.sidebar.toggle("Dark Mode", False, on_change=ChangeTheme)


if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()


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


# Define function to convert list to tuple for SQL query
def query_tuple(list_):
    return str(tuple(list_)).replace(',)', ')')

# Define query to get hospital data
if len(provider_types) != 0 and min_hospital_beds < max_hospital_beds:
    query = f"""
        SELECT name, hd.provider_type_code, hd.bed_count AS beds_number, latitude, longitude
        FROM hospital_locations AS hl
        JOIN hospital_details AS hd ON hl.hospital_id = hd.hospital_id
        WHERE hd.bed_count >= {min_hospital_beds}
        AND hd.bed_count <= {max_hospital_beds}
        AND hd.provider_type_code IN {query_tuple(provider_types)}
        """

    # Read data from database to dataframe
    engine = establish_connection_to_database()
    df_hospitals = pd.read_sql(query, engine)
else:
    # dummy data for empty map
    df_hospitals = pd.DataFrame({'name': ['dummy_1', 'dummy_2'], 'provider_type_code': ['O', 'O'], 'beds_number': [1, 2], 'latitude': [0.0, 0.0], 'longitude': [0.0, 0.0]})


# Get places
query = """
    SELECT name, latitude, longitude, zip
    FROM places
    """
df_places = pd.read_sql(query, engine)
df_places['zip'] = df_places['zip'].astype(int)


with st.container():
    col1, col2, col3 = st.columns([1, 10, 1])


    with col2:

        # Create a menu to navigate between the pages
        selected = option_menu(
        menu_title=None,
        options = ["Home", "Hospital Map"],
        icons = ["house", "map"],
        menu_icon = "cast",
        orientation = "horizontal")

        # Create figures        
        if "mapstyle" not in ms:
            mapstyle = 'open-street-map'
        else:
            mapstyle = ms.mapstyle

        fig_hospitals = create_hospital_map_new(df_hospitals, mapstyle)
        fig_places = create_places_map(df_places, mapstyle)

        st.markdown(
            """
            <style>
            .stPlotlyChart {
                border-radius: 15px;  /* Set your desired border-radius here */
                overflow: hidden;      /* Ensure the border-radius is applied properly */
                margin: 0px 0px 0px 0px;            /* Remove padding */
            }
            </style>
            """,
            unsafe_allow_html=True
            )

        # Render the Plotly chart
        st.markdown(f"<h2 style='text-align: center; padding: 10'>{cont[lang]['hospital_map_title']}</h2>", unsafe_allow_html=True)
        st.plotly_chart(fig_hospitals, use_container_width=True)
        st.markdown(f"<h2 style='text-align: center; padding: 10'>{cont[lang]['hospital_map_title']}</h2>", unsafe_allow_html=True)
        st.plotly_chart(fig_places, use_container_width=True)