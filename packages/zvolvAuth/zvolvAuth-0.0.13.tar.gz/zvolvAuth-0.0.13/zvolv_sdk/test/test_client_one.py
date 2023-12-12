import pytest
from unittest.mock import patch, MagicMock
from zvolv_sdk.client_one import Client_one  # Import the class containing the login method

@pytest.fixture
def mock_load_token_cache(requests_mock):
    # Arrange
    return MagicMock(return_value={})  # Mock the load_token_cache method

@pytest.fixture
def mock_save_token_cache(requests_mock):
    # Arrange
    return MagicMock()  # Mock the save_token_cache method

@pytest.fixture
def mock_requests_post_success(requests_mock):
    # Arrange
    mock_url = 'https://yogeshjadhav.zvolv.co/rest/v17/user/login'
    mock_response = {'token': 'mock_token'}
    requests_mock.post(mock_url, json=mock_response)
    return mock_response

@pytest.fixture
def instance(mock_load_token_cache, mock_save_token_cache):
    # Arrange
    with patch.object(Client_one, 'load_token_cache', mock_load_token_cache):
        with patch.object(Client_one, 'save_token_cache', mock_save_token_cache):
            instance = Client_one()  # Create an instance of your class
    return instance

def test_login_successful(instance, mock_requests_post_success):
    # Arrange
    instance.load_token_cache.side_effect = [{}]

    # Act
    result = instance.login()

    # Assert
    assert result == mock_requests_post_success
    instance.save_token_cache.assert_called_once()  # Assert that save_token_cache is called

# Add more test cases for different scenarios, such as cache hit, failure, etc.
