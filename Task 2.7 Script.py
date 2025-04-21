############################################## Library Imports #########################################################

import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime as dt
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
from PIL import Image

################################### Initial Settings for Dashboard ####################################################

st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title("Citi Bike Strategy Dashboard")

# define side bar
st.sidebar.title("Tab Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis:',
  ["Intro Page","Weather and Bike Usage",
   "Trips by Season", "Most Popular Stations",
    "Interactive Map with Aggregated Bike Trips", "Recommendations"])

########################## Import Data #################################################################################

dtype_mapping = {6: str, 8: str} # force columns as string data types
df = pd.read_csv('Data_Smallest_Sample.csv', dtype=dtype_mapping)
top20 = pd.read_csv('Top_20.csv', index_col = 0)
map_df = pd.read_csv('Map_df.csv', index_col = 0)

####################################### Dedfine the Pages ##############################################################


# Intro Page

if page == "Intro Page":
    st.markdown("#### This dashboard aims to provide helpful insights on the expansion problems Citi Bike currently faces.")
    st.markdown("Right now, Citi Bike runs into a situation where customers complain about bikes not being available at certain times and locations. This analysis will look at the potential reasons behind this. The dashboard is separated into 5 sections:")
    st.markdown("- Weather and Bike Usage")
    st.markdown("- Trips by Season")
    st.markdown("- Most Popular Stations")
    st.markdown("- Interactive Map with Aggregated Bike Trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Tab Selector' will take you to the different aspects of the analysis.")

    myImage = Image.open("Intro Photo.jpg") #source: https://unsplash.com/photos/bicycles-parked-on-the-side-of-a-street-KcOoW1Tv06Q
    st.image(myImage)

# Weather and Bike Usage Page
    
elif page == 'Weather and Bike Usage':

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # line chart
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['trip_count'],
        name='Daily Bike Rides',
        line=dict(color='blue')
    ),
    secondary_y=False
    )

    fig2.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['avgTemp'],
        name='Daily Temperature (C)',
        line=dict(color='red')
    ),
    secondary_y=True
    )

    fig2.update_layout(
    title_text='Daily Bike Rides vs. Temperature',
    title_x=0.5, # centers the title
    height=400
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship to the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be more of an issue in the warmer months, from May to October.")

# Trips by Season Page
    
elif page == 'Trips by Season':

    season_counts = df['season'].value_counts().reindex(['winter', 'spring', 'summer', 'fall'])

    # bar chart
    fig = px.bar(
    x=season_counts.index,
    y=season_counts.values,
    labels={'x': 'Season', 'y': 'Total Rides'},
    title='Total Rides by Season',
    color=season_counts.index,
    color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("This chart shows a surprising trend that the shoulder seasons, Spring and Fall, have less riders than the summer and winter months. This warrents further investigation as perhaps it correlates with school schedules or popular tourism times.")

# Most Popular Stations Page
    
    # create season variable

elif page == 'Most Popular Stations':
    
    # bar chart
    # define five shades of purple from light to dark
    colors = ['#f2e5f7', '#d9b3e6', '#bf80cc', '#9933b2', '#660066']
    # create bins to categorize 'value' into 5 groups
    bins = np.linspace(top20['value'].min(), top20['value'].max(), 6)  # 6 edges = 5 bins
    color_indices = np.digitize(top20['value'], bins) - 1  # indices from 0 to 4
    # ensure indices stay within 0-4
    color_indices = np.clip(color_indices, 0, 4)
    # map each bar to one of the 5 colors
    discrete_colors = [colors[i] for i in color_indices]
    # create bar chart
    fig3 = go.Figure(go.Bar(
        x=top20['start_station_name'],
        y=top20['value'],
        marker=dict(color=discrete_colors)
    ))

    fig3.update_layout(
    title = 'Top 20 Bike Stations NYC',
    xaxis_title = 'Start Stations',
    yaxis_title ='Sum of Trips',
    width = 900, height = 400
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St. There is a big jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")

# Interactive Map with Aggregated Bike Trips Page

elif page == 'Interactive Map with Aggregated Bike Trips': 

    # import map

    st.write("Interactive Map Showing Bike Trips in NYC")

    path_to_html = "Final_Map_Editable.html" 

    # read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    # add loading spinner
    with st.spinner('Loading map...'):
        st.components.v1.html(html_data, height=1000)

    # show in webpage
    st.header("Aggregated Bike Trips in NYC")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown(" W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St. While having the aggregated bike trips filter enabled, we can see that W 21 St & 6 Ave and West St & Chambers St are popular start stations and account for the most commonly taken trips. However, this does not hold true for Broadway & W 58 St.")
    st.markdown("The most common routes (>6,000) are in the heart of the city surrounding the tourist areas like the Empire State Building, Union Square, Grand Central Station, Broadway, etc.")

else:
    
    st.header("Conclusions and Recommendations")
    bikes = Image.open("Conclusion Photo.jpg")  #source: https://unsplash.com/photos/several-vehicle-parked-beside-building-uzkjyuWEB7Y
    st.image(bikes)
    st.markdown("### Our analysis has shown that Citi Bike should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations in the heart of the city. A limitation of this study is how many bikes are able to be parked in each station. Perhaps rather than adding more stations, adding to current stations capacities would provide an adequate response.")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand and reduce supply during other seasons.")


