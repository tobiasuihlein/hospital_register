from taipy.gui import Gui
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

page = """
# Hospital Analysis Dashboard
## Hospital Distance Map
<|{min_hospital_beds}|slider|on_change=on_slider|min=0|max=1000|step=50|change_delay=1|>
<|{data}|chart|type=scattermapbox|plot_config={config}|options={options}|layout={layout_map}|lat=latitude|lon=longitude|mode=markers|height=100%|>
"""

# Read data from SQL database into a DataFrame
load_dotenv()
DB_PW = os.getenv('DB_PW')

username = 'root'
password = DB_PW
host = 'localhost'
port = '3306'
database = 'hospital_register'

engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

min_hospital_beds = 300

query = f"""
    SELECT name, beds_number, latitude, longitude
    FROM hospital_locations
    WHERE beds_number > {min_hospital_beds}
    """

data = pd.read_sql(query, engine)

layout_map = {
    'mapbox': {'style': 'open-street-map', 'center': {'lat': 51.2, 'lon': 10.5}, 'zoom': 4}
}

options = {
    'marker': {
        'size': data['beds_number'] / 10,  # Adjust size for better visualization
        'color': data['beds_number'],  # Use beds_number for color
        'colorscale': 'OrRd',
        'colorbar': {'title': 'Number of Beds'}
    }
}

config = {
    'displayModeBar': True,
    'responsive': True
}


def on_slider(state):
    query = f"""
    SELECT name, beds_number, latitude, longitude
    FROM hospital_locations
    WHERE beds_number > {state.min_hospital_beds}
    """
    state.data = pd.read_sql(query, engine)

if __name__ == "__main__":
    Gui(page).run(dark_mode=True, use_reloader=True)