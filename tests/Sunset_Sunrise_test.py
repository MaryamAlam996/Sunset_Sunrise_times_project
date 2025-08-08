import pytest
import pandas as pd

import pytest
from unittest.mock import patch, Mock, MagicMock
import requests
from unittest.mock import patch
from requests.exceptions import Timeout, RequestException
import pandas as pd


from scripts.Sunset_Sunrise import get_country_data
from scripts.Sunset_Sunrise import get_sunrise_sunset
from scripts.Sunset_Sunrise import load_df
from scripts.Sunset_Sunrise import create_sunset_sunrise_csv
from scripts.Sunset_Sunrise import Find_sunset_sunrise_info


# testing the get_country_data function
def test_get_country_data():
    # Arrange
    test_df = df = pd.DataFrame(columns=['Country','Latitude','Longitude','D','E','F','G'])
    expected_columns = ['Country', 'Latitude', 'Longitude']
    expected_df = pd.DataFrame(columns=expected_columns)
    # Act
    actual_df = get_country_data(test_df)
    # Assert
    #  check is dataframes have same number of columns
    assert len(actual_df.columns) == len(expected_columns)

# testing the get_sunrise_sunset function for successful response
@patch('scripts.Sunset_Sunrise.requests.get')
def test_get_sunrise_sunset_response_200(mock_get):
    # Arrange
    # Sample mock JSON data the API would return
    mock_json_data = {
        'results': {
            'sunrise': '11:00:00 AM',
            'sunset': '10:26:35 PM',
            'day_length': '11:26:35'
        },
        'status': 'OK',
        'tzid': 'UTC'
    }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_json_data
    mock_get.return_value = mock_response
    # Act
    result = get_sunrise_sunset(0, 0, "2024-01-01")
    # Assert
    assert isinstance(result, dict)
    assert result['sunrise'] == '11:00:00 AM'
    assert result['sunset'] == '10:26:35 PM'
    assert result['day_length'] == '11:26:35'


# testing the get_sunrise_sunset function with a non-200 response
@patch('scripts.Sunset_Sunrise.requests.get')
def test_get_sunrise_sunset_response_other(mock_get):
    # Arrange
    # Sample mock JSON data the API would return
    mock_json_data = {
        'results': {
            'sunrise': '11:00:00 AM',
            'sunset': '10:26:35 PM',
            'day_length': '11:26:35'
        },
        'status': 'OK',
        'tzid': 'UTC'
    }
    mock_response = Mock()
    mock_response.status_code = 404 # Simulating a non-200 response
    mock_response.json.return_value = mock_json_data
    mock_get.return_value = mock_response
    # Act
    # check if the function raises a RequestException
    with pytest.raises(RequestException):
        get_sunrise_sunset(0, 0, "2024-01-01")


# testing the get_sunrise_sunset function with a timeout    
@patch('scripts.Sunset_Sunrise.requests.get')
def test_get_sunrise_sunset_response_time_out(mock_get):
    # Arrange
    # Sample mock JSON data the API would return
    mock_json_data = {
        'results': {
            'sunrise': '11:00:00 AM',
            'sunset': '10:26:35 PM',
            'day_length': '11:26:35'
        },
        'status': 'OK',
        'tzid': 'UTC'
    }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_json_data
    mock_get.return_value = mock_response
    mock_get.side_effect = Timeout  # Simulating a timeout
    # Act
    with pytest.raises(Timeout):
        get_sunrise_sunset(0, 0, "2024-01-01")


# testing the get_sunrise_sunset function with an unkown error
@patch('scripts.Sunset_Sunrise.requests.get')
def test_get_sunrise_sunset_response_time_out(mock_get):
    # Arrange
    # Sample mock JSON data the API would return
    mock_json_data = {
        'results': {
            'sunrise': '11:00:00 AM',
            'sunset': '10:26:35 PM',
            'day_length': '11:26:35'
        },
        'status': 'OK',
        'tzid': 'UTC'
    }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_json_data
    mock_get.return_value = mock_response
    mock_get.side_effect = Exception("Unknown error")  # Simulating an unknown error
    # Act
    with pytest.raises(Exception):
        get_sunrise_sunset(0, 0, "2024-01-01")
    

# testing the get_sunrise_sunset function with an unexpected data format
@patch('scripts.Sunset_Sunrise.requests.get')
def test_get_sunrise_sunset_response_not_dict(mock_get):
    # Arrange
    # Sample mock JSON data the API would return
    mock_json_data = 5
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_json_data
    mock_get.return_value = mock_response
    # Act
    with pytest.raises(ValueError):
        get_sunrise_sunset(0, 0, "2024-01-01")

# def Example():

@patch('scripts.Sunset_Sunrise.pd.read_csv')
@patch('scripts.Sunset_Sunrise.get_country_data')
def test_load_df(mock_country_data, mock_read_csv):
    # Arrange
    mock_data = pd.DataFrame({
        'Country': ['Country1', 'Country2'],
        'Latitude': [10.0, 20.0],
        'Longitude': [30.0, 40.0],
    })
    mock_read_csv.return_value = mock_data
    mock_country_data.return_value = mock_data
    # action
    result_df = load_df()
    # Assert
    assert isinstance(result_df, pd.DataFrame)
    

# @patch('scripts.Sunset_Sunrise.load_df')
# def test_Find_sunset_sunrise_info(mock_load_df):
#     mock_df = 
#     mock_load_df.return_value = mock_df
    
@patch('scripts.Sunset_Sunrise.load_df') 
@patch('scripts.Sunset_Sunrise.get_sunrise_sunset')    
def test_Find_sunset_sunrise_info(mock_get_sun, mock_load_df):
    mock_df = pd.DataFrame({
        "Country": ["A"],
        "Latitude": [10.0],
        "Longitude": [20.0]
    })

    # Mock sunrise/sunset API response
    mock_sun_data = {
        "sunrise": "06:00:00",
        "sunset": "18:00:00",
        "day_length": "12:00:00"
    }

    mock_load_df.return_value = mock_df
    mock_get_sun.return_value = mock_sun_data
    # Act
    result_df = Find_sunset_sunrise_info()

    # type check
    assert isinstance(result_df, pd.DataFrame)
    
    # expected number of rows 
    assert len(result_df) == 12
    
    # correct columns
    expected_cols = ['Country', 'Date', 'Latitude', 'Longitude', 'Sunrise', 'Sunset', 'Day_length']
    assert list(result_df.columns) == expected_cols

# for none returned by API
@patch('scripts.Sunset_Sunrise.load_df') 
@patch('scripts.Sunset_Sunrise.get_sunrise_sunset')    
def test_Find_sunset_sunrise_info_none(mock_get_sun, mock_load_df):
    mock_df = pd.DataFrame({
        "Country": ["A"],
        "Latitude": [10.0],
        "Longitude": [20.0]
    })

    # Mock sunrise/sunset API response
    mock_sun_data = None

    mock_load_df.return_value = mock_df
    mock_get_sun.return_value = mock_sun_data
    # Act
    result_df = Find_sunset_sunrise_info()

    # type check
    assert isinstance(result_df, pd.DataFrame)
    
    # expected number of rows 
    assert len(result_df) == 0
    
    # empty df
    assert result_df.empty
    
@patch('scripts.Sunset_Sunrise.Find_sunset_sunrise_info') 
@patch('scripts.Sunset_Sunrise.pd.DataFrame.to_csv')
def test_create_sunset_sunrise_csv(mock_to_csv, mock_find_info, capsys):
    mock_find_info.return_value = Mock()
    mock_to_csv.return_value = Mock()
    TEST_MODE = False
    # act
    create_sunset_sunrise_csv(TEST_MODE)
    captured = capsys.readouterr()
    assert "Data saved to sunrise_sunset_data_2.csv"
    
# for test mode
@patch('scripts.Sunset_Sunrise.Find_sunset_sunrise_info') 
@patch('scripts.Sunset_Sunrise.pd.DataFrame.to_csv')
def test_create_sunset_sunrise_csv(mock_to_csv, mock_find_info, capsys):
    mock_find_info.return_value = Mock()
    mock_to_csv.return_value = Mock()
    TEST_MODE = False
    # act
    create_sunset_sunrise_csv(TEST_MODE)
    captured = capsys.readouterr()
    assert "Data saved to sunrise_sunset_data_test.csv"