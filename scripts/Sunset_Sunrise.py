import requests
import pandas as pd
import time

# https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400
TEST_MODE = False


# Function to get country data from a CSV file
def get_country_data():
    df = pd.read_csv('Data/longitude-latitude.csv')
    # select only the columns we need
    edit_df = df[['Country', 'Latitude', 'Longitude']]
    # if TEST_MODE is True dataframe will only contain the first 5 rows
    if TEST_MODE:
        edit_df = edit_df.head(5)
    return edit_df


# Function to get sunrise and sunset times for
# a given latitude, longitude, and date
def get_sunrise_sunset(lat, lng, date):
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={date}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        return None


# Function to convert the results into a DataFrame
def Convert_to_df(x):
    df = pd.DataFrame.from_dict(x, orient='index', columns=['Value'])
    return df


# Example use of the get_sunrise_sunset function
def Example():
    # Example coordinates for Malaga, Spain
    TEST = get_sunrise_sunset(36.7201600, -4.4203400, "2024-01-01")
    TEST = Convert_to_df(TEST)
    print(TEST)
    return TEST


def Find_sunset_sunrise_info():
    df = get_country_data()
    df = df.reset_index(drop=True)
    # empty new df
    Coord_df = pd.DataFrame(columns=['Country', 'Date', 'Latitude', 'Longitude', 'Sunrise', 'Sunset','Day_length'])
    Coord_list = []
    i = -1
    for index, row in df.iterrows():
        time.sleep(1)
        # print(row['Country'], row['Latitude'], row['Longitude'])
        # Coord_list.append([row['Latitude'],row['Longitude']])
        
        for month in range(1, 13):
            i = i + 1
            print(month)
            sunrise_sunset = get_sunrise_sunset(row['Latitude'], row['Longitude'], f'2024-{month:02d}-01')
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
                print(Coord_list[i])

    Coord_df = pd.DataFrame(Coord_list)
    return Coord_df


# Function to create a CSV file with the sunset and sunrise data
def create_sunset_sunrise_csv():
    Coord_df = Find_sunset_sunrise_info()
    Coord_df.to_csv('Data/sunrise_sunset_data_3.csv', index=False)
    print("Data saved to sunrise_sunset_data_3.csv")

# Example()

create_sunset_sunrise_csv()


