import requests
import pandas as pd
import time

# https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400
TEST_MODE = False


# Function to get country data from a CSV file
def get_country_data(df):
    # select only the columns we need
    edit_df = df[['Country', 'Latitude', 'Longitude']]
    # if TEST_MODE is True dataframe will only contain the first 5 rows
    if TEST_MODE:
        edit_df = edit_df.head(5)
    return edit_df


# Function to get sunrise and sunset times for
# a given latitude, longitude, and date
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


# function to load data as a dataframe
def load_df():
    df = pd.read_csv('Data/longitude-latitude.csv')
    df = get_country_data(df)
    df = df.reset_index(drop=True) 
    return df


# function to find sunrise and sunset information for all countries
def Find_sunset_sunrise_info():
    df = load_df()
    # empty new df
    Coord_df = pd.DataFrame(
        columns=[
            'Country', 'Date', 'Latitude', 'Longitude',
            'Sunrise', 'Sunset', 'Day_length'
        ]
    )
    Coord_list = []
    # i = -1
    print("Processing countries for sunrise and sunset data...")
    for index, row in df.iterrows():
        time.sleep(1)
        for month in range(1, 13):
            # i = i + 1
            sunrise_sunset = get_sunrise_sunset(
                row['Latitude'],
                row['Longitude'],
                f'2024-{month:02d}-01'
            )
            if sunrise_sunset:
                Coord_list.append({
                    'Country': row['Country'],
                    'Date': f'2024-{month:02d}-01',
                    'Latitude': row['Latitude'],
                    'Longitude': row['Longitude'],
                    'Sunrise': sunrise_sunset['sunrise'],
                    'Sunset': sunrise_sunset['sunset'],
                    'Day_length': sunrise_sunset['day_length']
                })
        print(f"Processed {index + 1} countries")
    Coord_df = pd.DataFrame(Coord_list)
    return Coord_df


# Function to create a CSV file with the sunset and sunrise data
def create_sunset_sunrise_csv(TEST_MODE):
    Coord_df = Find_sunset_sunrise_info()
    print("Saving data to CSV file...")
    if TEST_MODE:
        Coord_df.to_csv('Data/sunrise_sunset_data_test.csv', index=False)
        print("Data saved to sunrise_sunset_data_test.csv")
    else:
        Coord_df.to_csv('Data/sunrise_sunset_data_2.csv', index=False)
        print("Data saved to sunrise_sunset_data_2.csv")

# if TEST_MODE:
    # print("Running in test mode...")
# create_sunset_sunrise_csv()

if __name__ == "__main__":
    # Code here only runs if you run: python scripts/Sunset_Sunrise.py
    print("Running in test mode...")
    create_sunset_sunrise_csv(TEST_MODE)
