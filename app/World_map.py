import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import requests

color_continuous_scale = [
    [0.0, "#330988"],    # 00:00
    [0.25, "#91e0ff"],   # 06:00
    [0.5, "#ffff00"],    # 12:00
    [0.75, "#ff0099"],   # 18:00
    [1.0, "#330988"]     # 24:00
]
color_continuous_scale_2 = [
    [0.0, "#00EEFF"],
    [1, "#F700FF"]
]


# Function to get sunrise and sunset times for
# a given latitude, longitude, and date
# using the API from https://sunrise-sunset.org/api
def get_sunrise_sunset(lat, lng, date):
    url = (
        f"https://api.sunrise-sunset.org/json"
        f"?lat={lat}&lng={lng}&date={date}"
    )
    # response = requests.get(url, timeout=10)

    # if response.status_code == 200:
    #     data = response.json()
    #     return data['results']
    # else:
    #     return None
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # print(data)
            # print(isinstance(data, dict))
            if isinstance(data, dict):
                return(data['results'] )
            else:
                raise ValueError("Unexpected data format received from API.")
        else:
            # error handling for non-200 status codes
            raise requests.exceptions.RequestException(
                f"Error fetching data: {response.status_code}"
            )
    except requests.exceptions.Timeout:
        print(f"Error: Request to {url} timed out.")
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        raise
    return None


# Function to convert time strings in series to seconds
def convert_to_seconds(series):
    return series.apply(lambda x: _time_str_to_seconds(x))


# Function to convert a time string to seconds
def _time_str_to_seconds(time_str):
    # Convert the time string to a datetime object
    dt = datetime.strptime(time_str, "%I:%M:%S %p")
    # Calculate the total seconds from the datetime object
    seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    return seconds


def _time_str_to_seconds(time_str):
    if not isinstance(time_str, str):
        raise TypeError(f"Expected a string for time_str, got {type(time_str).__name__} instead.")
    
    formats = ("%I:%M:%S %p", "%H:%M:%S")
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            return dt.hour * 3600 + dt.minute * 60 + dt.second
        except ValueError:
            pass

    raise ValueError(f"Invalid time string: {time_str}")


# Function to convert sunrise, sunset, and day length times to seconds
def times_to_int(df):
    # Convert sunrise, sunset, and day length times to seconds
    df['Sunrise_seconds'] = convert_to_seconds(df['Sunrise'])
    df['Sunset_seconds'] = convert_to_seconds(df['Sunset'])
    # Calculate the day length in seconds
    df['Day_length_seconds'] = df['Sunset_seconds'] - df['Sunrise_seconds']
    # convert to positive numbers
    df['Day_length_seconds'] = df['Day_length_seconds'].abs()
    return df


# Function to create a map of sunrise times
def sunrise_map(df, selected_date):
    fig = px.scatter_mapbox(
        df,
        lat="LAT",
        lon="LON",
        color="Sunrise_seconds",
        zoom=1,
        height=600,
        mapbox_style="carto-positron",
        color_continuous_scale=color_continuous_scale,
        range_color=(0, 86400),
            hover_name="Country",
        hover_data={"Sunrise_seconds": False, "Sunrise": True}
    )
    # display the map
    st.title(f"Sunrise Times for {selected_date}")
    st.plotly_chart(fig, use_container_width=True)


# function to create a map of sunset times
def sunset_map(df, selected_date):
    fig2 = px.scatter_mapbox(
        df,
        lat="LAT",
        lon="LON",
        color="Sunset_seconds",
        zoom=1,
        height=600,
        mapbox_style="carto-positron",
        color_continuous_scale=color_continuous_scale,
        range_color=(0, 86400),
            hover_name="Country",
        hover_data={"Sunset_seconds": False, "Sunset": True}
    )
    # display the map
    st.title(f"Sunset Times for {selected_date}")
    st.plotly_chart(fig2, use_container_width=True)


# function to create a map of day lengths
def day_length_map(df, selected_date):
    fig3 = px.scatter_mapbox(
        df,
        lat="LAT",
        lon="LON",
        color="Day_length_seconds",
        zoom=1,
        height=600,
        mapbox_style="carto-positron",
        color_continuous_scale=color_continuous_scale_2,
        range_color=(0, 86400),
            hover_name="Country",
        hover_data={"Day_length_seconds": False, "Day_length": True}
    )
    # display the map
    st.title(f"Day lengths for {selected_date}")
    st.plotly_chart(fig3, use_container_width=True)


# Function to create a world map with sunrise, sunset, and day length data
def world_map():
    # load data
    df = pd.read_csv('../data/sunrise_sunset_data_2.csv')
    # rename columns
    df.rename(columns={"Latitude": "LAT", "Longitude": "LON"}, inplace=True)
    # remove null values
    df.dropna(inplace=True)
    # st.dataframe(df)
    # create a map
    # st.map(df)
    # convert times in the df to seconds
    times_to_int(df)
    # select a date from df
    selected_date = st.selectbox(
        "Select a date",
        df['Date'].unique()
    )
    # filter df by selected date
    df = df[df['Date'] == selected_date]
    # select a map to display
    selected_option = st.selectbox(
        "Select a map to display",
        ["Sunrise", "Sunset", "Day Length"]
    )
    # display the selected map
    if selected_option == "Sunrise":
        sunrise_map(df, selected_date)
    elif selected_option == "Sunset":
        sunset_map(df, selected_date)
    else:
        day_length_map(df, selected_date)

    # st.dataframe(df)


# Function to create a country map with a chosen country and date
def country_map():
    st.divider()
    # load data
    df = pd.read_csv('../data/longitude-latitude.csv')
    df.rename(columns={"Latitude": "LAT", "Longitude": "LON"}, inplace=True)
    # st.dataframe(df)
    # select a country
    selected_country = st.selectbox(
        "Select a country",
        df['Country'].unique()
    )
    # write in a date
    selected_date = st.date_input(
        "Select a date",
        value=pd.to_datetime("2023-01-01"),
        min_value=pd.to_datetime("2020-01-01"),
        max_value=pd.to_datetime("2024-12-31")
    )
    # filter df by selected country
    df_country = df[df['Country'] == selected_country].copy()
    # get sunrise and sunset times for the selected country and date
    # Extract single latitude and longitude values from the filtered DataFrame
    lat = df_country.iloc[0]["LAT"]
    lon = df_country.iloc[0]["LON"]

    # get sunrise and sunset times for the selected country and date
    sunrise_sunset = get_sunrise_sunset(
        lat,
        lon,
        selected_date
    )

    # Add sunrise, sunset, and day length to the df_country dataframe
    df_country["Sunrise"] = sunrise_sunset['sunrise']
    df_country["Sunset"] = sunrise_sunset['sunset']
    df_country["Day_length"] = sunrise_sunset['day_length']
    df_country["selected_date"] = selected_date.strftime("%Y-%m-%d")
    # Create a scatter mapbox plot for the selected country
    fig_a = px.scatter_mapbox(
        df_country,
        lat="LAT",
        lon="LON",
        zoom=3,
        height=600,
        mapbox_style="carto-positron",
        hover_name="Country",
        hover_data={
            "LAT": False,
            "LON": False,
            "selected_date": True,
            "Sunrise": True,
            "Sunset": True,
            "Day_length": True
        }
    )
    # display the map
    st.title(f"Map of {selected_country}")
    st.plotly_chart(fig_a, use_container_width=True)
