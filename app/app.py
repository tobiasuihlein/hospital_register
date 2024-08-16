from taipy.gui import Gui, notify
import taipy.gui.builder as tgb
import pandas as pd
from functions import create_map
from functions import establish_connection_to_database

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

fig = create_map(df_hospitals)

# Define callback function for min_hospital_beds slider
def on_slider(state):
    query = f"""
    SELECT name, beds_number, latitude, longitude
    FROM hospital_locations
    WHERE beds_number > {state.min_hospital_beds}
    """
    state.df_hospitals = pd.read_sql(query, engine)
    state.fig = create_map(state.df_hospitals)
    return state.fig


mapstyle = 'carto-positron'

def on_change(state, var_name, var_value):
    if var_name == "theme" and var_value:
        state.mapstyle = "carto-darkmatter"
        notify(state, "info", "Switched to Dark Mode")
    elif var_name == "theme" and not var_value:
        state.mapstyle = "carto-positron"
        notify(state, "info", "Switched to Light Mode")


# Create GUI
with tgb.Page() as page:
    with tgb.layout(columns = '1 3 1', gap = '10px'):

        with tgb.part():
            tgb.html("h1", "") # placeholder

        with tgb.part():
            tgb.html("h1", "Klinikatlas Analysis Dashboard")

            tgb.html("p", f"Minimum number of beds")
            tgb.text("{min_hospital_beds}", mode='md')
            tgb.slider(label="min_hospital_beds",
               value="{min_hospital_beds}", min=0, max=1000, step=10,
               change_delay=10, on_change=on_slider)

            tgb.chart(figure="{fig}")
            
        with tgb.part():
            tgb.html("h1", "") # placeholder
            tgb.toggle(theme=True)
            
            

# Run GUI
if __name__ == "__main__":
    Gui(page).run(dark_mode=True, use_reloader=True)