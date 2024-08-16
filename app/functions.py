import plotly.graph_objects as go

# Define function to create hospitals map
def create_map(df_hospitals):
    # Normalize the marker sizes
    min_beds = 0
    max_beds = 1500
    min_size = 3
    max_size = 25
    normalized_sizes = (df_hospitals['beds_number'] - min_beds) / (max_beds - min_beds) * (max_size - min_size) + min_size

    # Create the second layer with a color scale and scaled marker sizes
    second_layer = go.Scattermapbox(
        lat=df_hospitals['latitude'],
        lon=df_hospitals['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=normalized_sizes,  # Scaled size of the markers
            color=df_hospitals['beds_number'],  # Column for color scale
            colorscale='Blugrn',  # Specify the color scale
            cmin=min_beds,  # Set the minimum value for the colorscale
            cmax=max_beds,  # Set the maximum value for the colorscale
            colorbar=dict(
                title=dict(text="Hospital [number of beds]", side="top"),
                orientation='h',  # Horizontal orientation
                x=0.5,  # Center horizontally
                y=-0.25  # Position below the first colorbar
            )
        ),
        text=df_hospitals['name'],  # Hover text
        hoverinfo='text',
            hovertemplate=(
            "<b>Hospital:</b> %{text}<br>" +
            "<b>Number of beds:</b> %{marker.color}"
        ),
        showlegend=False,
        name=''
    )

    # Create the figure and add both layers
    fig = go.Figure()
    fig.add_trace(second_layer)

    # Update the layout
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # Map style
            center=dict(lat=51.2, lon=10.5),  # Center of the map
            zoom=4.8  # Initial zoom level
        ),
        width=600,  # Set width in pixels
        height=800  # Set height in pixels
    )

    return fig

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


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