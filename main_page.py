"""
# My first app
Here"s our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np 

st.title("Uber pickups in NYC")

#%% fetch some data

DATE_COLUMN = "date/time"
DATA_url = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data # cache data so that it is not loaded every time the page is refreshed
def load_data(nrows):
    data = pd.read_csv(DATA_url, nrows=nrows) # read data from url
    lowercase = lambda x: str(x).lower() # create a lambda function to lowercase all column names 
    data.rename(lowercase, axis="columns", inplace=True) # rename columns to lowercase
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) # convert to datetime
    return data 

data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#%% draw a histogram 
st.subheader("Number of pickups by hour")

hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] # create a histogram of the data 
st.bar_chart(hist_values)

#%% plot data on a map
st.subheader("Map of all pickups")
st.map(data)

hour_to_filter = st.slider("hour", 0, 23, 6) # add a slider to the sidebar
filtered_data = data[data[DATE_COLUMN].dt.hour == 23] # filter data by hour 
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)


