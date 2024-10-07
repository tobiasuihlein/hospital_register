from taipy.gui import Gui, notify
import taipy.gui.builder as tgb
import pandas as pd
from app_functions import create_map, establish_connection_to_database
import threading

mapstyle = 'open-street-map'

# Connect to  database
engine = establish_connection_to_database()

# Define query to get hospital data
min_hospital_beds = 500
query = f"""
    SELECT name, beds_number, latitude, longitude
    FROM hospital_locations
    WHERE beds_number > {min_hospital_beds}
    """

# Read data from database to dataframe
df_hospitals = pd.read_sql(query, engine)

# Store initial min and max values of beds_number
initial_min_beds = 0
initial_max_beds = df_hospitals['beds_number'].max()

fig = create_map(df_hospitals, mapstyle)

# Define callback function for min_hospital_beds slider
# Create a lock for thread safety
lock = threading.Lock()

# Define callback function for min_hospital_beds slider
def on_slider_beds_number_map(state):
    with lock:
        try:
            query = f"""
            SELECT name, beds_number, latitude, longitude
            FROM hospital_locations
            WHERE beds_number > {state.min_hospital_beds}
            """
            df_hospitals = pd.read_sql(query, engine)
            if not df_hospitals.empty:
                state.df_hospitals = df_hospitals
                state.fig = create_map(state.df_hospitals, mapstyle)
            else:
                print("Query returned no results.")
                state.fig = fig  # Fallback to the initial figure
        except Exception as e:
            print(f"Error updating slider state: {e}")
            state.fig = fig  # Fallback to the initial figure
    return state.fig


# Create GUI
with tgb.Page() as page:
    with tgb.layout(columns = '1 3 1', gap = '10px'):

        with tgb.part():
            tgb.html("h1", "") # placeholder

        with tgb.part():
            tgb.html("h1", "Klinikatlas Analysis Dashboard")

            tgb.text("Minimum number of beds: {min_hospital_beds}", mode='md')
            tgb.slider(label="min_hospital_beds",
               value="{min_hospital_beds}", min=0, max=1000, step=10,
               change_delay=100, on_change=on_slider_beds_number_map)
            
            tgb.toggle(label="Filter Departments", value=False, allow_unselect=True)
            tgb.selector(label="Select Department", dropdown=True, lov=['dep_1', 'dep_2', 'dep_3'])
            tgb.chart(figure="{fig}")
            
        with tgb.part():
            tgb.html("h1", "") # placeholder
            tgb.toggle(theme=True)


# Run GUI
if __name__ == "__main__":
    Gui(page).run(dark_mode=False, use_reloader=True)