################################################ CITI BIKE DASHBOARD ############################################################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime as dt
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

########################### Initial Settings for the Dashboard ##################################################################

st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Citi Bike currently faces.")
st.markdown("Right now, Citi Bike runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

####################################### Import Data ###############################################################################

dtype_mapping = {6: str, 8: str}
df = pd.read_csv('Data_Smallest_Sample.csv', dtype=dtype_mapping)
top20 = pd.read_csv('Top_20.csv', index_col = 0)

########################################### Define the Charts #####################################################################

## Bar Chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Purples'}))

fig.update_layout(
    title = 'Top 20 Bike Stations NYC',
    xaxis_title = 'Start Stations',
    yaxis_title ='Sum of Trips',
    width = 900, height = 600
)

st.plotly_chart(fig, use_container_width=True)


## Line Chart

fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

fig_2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['trip_count'],
        name='Daily Bike Rides',
        line=dict(color='blue')
    ),
    secondary_y=False
)

fig_2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['avgTemp'],
        name='Daily Temperature (C)',
        line=dict(color='red')
    ),
    secondary_y=True
)

fig_2.update_layout(
    title_text = 'Daily Bike Rides vs. Temperature',
    title_x = 0.5,
    height = 600
)

st.plotly_chart(fig_2, use_container_width=True)

    
## Add Map

path_to_html = "bike_routes_map.html" 

# read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

# show in webpage
st.header("Aggregated Bike Trips in NYC")
st.components.v1.html(html_data,height=1000)