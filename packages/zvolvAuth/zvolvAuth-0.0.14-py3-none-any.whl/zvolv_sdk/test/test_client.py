import pytest
import requests_mock
from zvolv_sdk.client import Client

@pytest.fixture
def mock_requests_post_success(requests_mock):

    mock_url = 'https://yogeshjadhav.zvolv.co/rest/v17/user/login'
    mock_response = {'token': 'mock_token'}
    requests_mock.post(mock_url, json=mock_response)
    return mock_response

@pytest.fixture
def mock_requests_post_failure(requests_mock):
    mock_url = 'https://yogeshjadhav.zvolv.co/rest/v17/user/login'
    requests_mock.post(mock_url, status_code=401)  # Simulating a failed login
    return {'error': 'Authentication failed'}

def test_login_successful(mock_requests_post_success):
    instance = Client()  # Create an instance of your class
    result = instance.login()
    assert result == mock_requests_post_success

def test_login_failure(mock_requests_post_failure):
    instance = Client()  # Create an instance of your class
    with pytest.raises(Exception):
        instance.login()



# @pytest.fixture
# def mock_requests_post(requests_mock):
#     # Arrange
#     mock_url = 'https://yogeshjadhav.zvolv.co/rest/v17/user/login'
#     mock_response = {'token': 'mock_token'}
#     requests_mock.post(mock_url, json=mock_response)
#     return mock_response

# def test_login_successful(mock_requests_post):
#     instance = Client()  # Create an instance of your class
#     result = instance.login()
#     assert result == mock_requests_post

# def test_login_successful():
#     mock_url = 'https://yogeshjadhav.zvolv.co/rest/v17/user/login'
#     with requests_mock.Mocker() as m:
#         m.post(mock_url, status_code=200, json={'token': 'mock_token'})

#         instance = Client()
#         result = instance.login()
#         assert result == {'token': 'mock_token'}
