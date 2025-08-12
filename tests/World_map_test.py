import pytest
import pandas as pd

import pytest
from unittest.mock import patch, Mock, MagicMock
import requests
from unittest.mock import patch
from requests.exceptions import Timeout, RequestException
import pandas as pd
import plotly.express as px

from app.World_map import get_sunrise_sunset
from app.World_map import convert_to_seconds
from app.World_map import _time_str_to_seconds
from app.World_map import times_to_int
from app.World_map import sunrise_map
from app.World_map import sunset_map
from app.World_map import day_length_map
from app.World_map import  world_map
from app.World_map import country_map



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
        
#  testing to see if the lambda function is returning the correct series
@patch('app.World_map._time_str_to_seconds')     
def test_convert_to_seconds(mock_function):
    mock_list = [2, 2]
    mock_series = pd.Series(mock_list)
    mock_function.return_value = 1
    exp_list = [1,1]
    exp_series = pd.Series(exp_list)
    
    act_series = convert_to_seconds(mock_series)
    pd.testing.assert_series_equal(act_series, exp_series)

#  "sunrise":"7:27:02 AM",
# "sunset":"5:05:55 PM",
# "solar_noon":"12:16:28 PM",
# "day_length":"9:38:53",

@pytest.mark.parametrize("time_string, expected_seconds", [
    ("7:27:02 AM", 26822),   # 7*3600 + 27*60 + 2
    ("5:05:55 PM", 61555),   # 17*3600 + 5*60 + 55
    ("09:38:53", 34733)      # 9*3600 + 38*60 + 53
])
def test_time_str_to_seconds(time_string, expected_seconds):
    actual_output = _time_str_to_seconds(time_string)
    assert actual_output == expected_seconds
    
# error handling
def test_time_str_to_seconds_error():
    time_string = "Hello" # any invalid value but correct data type
    with pytest.raises(ValueError):
        _time_str_to_seconds(time_string)
        
def test_time_str_to_seconds_error():
    time_string = 0 # data type
    with pytest.raises(TypeError):
        _time_str_to_seconds(time_string)
   
   
def side_effect_func(x):
    return x*10

@patch("app.World_map.convert_to_seconds", side_effect=side_effect_func)
def test_times_to_int(mock_convert):
    data = {
        "Sunrise": [100, 200, 100],
        "Sunset": [100, 100, 200],
    }
    df = pd.DataFrame(data)

    data_expected = {
        "Sunrise": [100, 200, 100],
        "Sunset": [100, 100, 200],
        "Sunrise_seconds": [1000, 2000, 1000],
        "Sunset_seconds": [1000, 1000, 2000],
        "Day_length_seconds": [0, 1000, 1000]
    }
    exp_df = pd.DataFrame(data_expected)

    actual_df = times_to_int(df)
    pd.testing.assert_frame_equal(actual_df, exp_df)
    
    
    