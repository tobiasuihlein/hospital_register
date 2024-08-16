import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# Set page config to use full width
st.set_page_config(layout="wide")

# Streamlit app
st.title('Hospital Distance Map')

# Load and display the saved Plotly chart
with open("../resources/plotly_charts/hospital_distance_map.html", "r", encoding="utf-8") as f:
    html_chart = f.read()

# Allow overflow and auto resizing
html_with_border = f"""
    <div style="border: 1px solid lightgrey; padding: 5px; width: 100%; height: auto; overflow: hidden;">
        {html_chart}
    </div>
"""

# Display the chart with the border in Streamlit
st.components.v1.html(html_with_border, height=1200)
