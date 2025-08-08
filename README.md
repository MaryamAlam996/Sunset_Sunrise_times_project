# Sunset_Sunrise_times_project
A small project using the Sunset and sunrise times API
https://sunrise-sunset.org 

and the latitude and longitude csv https://www.kaggle.com/datasets/bohnacker/country-longitude-latitude/code

## Goals of project
- practice calling an API in python
- learn how to display data as a map in streamlit

## Sunset_Sunrise.py
Using the csv file a data frame of countries and their latitudes and longitudes is created. Using the API the sunrise, sunset and day length times can be found for a specific date, latitude and longitude. Combining both these resources, the sunset_sunrise script finds the sunset, sunrise and day length times for each country and for the first day of each month in the year 2024 (to show the differences in the times during the year). This data is then saved as a csv which is used in the streamlit app.

## World_map.py
Using the csv created, displays a map with points for each country which display information when you hover over them. The information shown can be filtered by what you would like to see (sunset times, sunrise times or the day lengths) as well as the time of year. The points are colour coordinated to easily compare. Underneath this map is another map which displays more specific data for each country. This is done by calling the API after selecting a country and a specific date, then a new map is generated showing the relevant information.

## Instructions to run
To run the streamlit app
```console
cd app
streamlit run main.py
```
To run the script for gathering data using the API
```console
python scripts/Sunset_Sunrise.py
```