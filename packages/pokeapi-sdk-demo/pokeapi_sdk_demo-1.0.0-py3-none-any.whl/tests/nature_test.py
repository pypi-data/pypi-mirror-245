import pytest
from pokeapi_sdk import PokeAPISDK, Nature
from requests.exceptions import HTTPError

@pytest.fixture
def api_client():
    return PokeAPISDK()

def test_get_nature(api_client):
    response = api_client.get_nature(1)
    assert isinstance(response, Nature), "The response should be a Nature instance"
    assert response.name == 'hardy', "The name of the Nature should be Hardy"

def test_invalid_nature(api_client):
    with pytest.raises(HTTPError):
        api_client.get_nature(-1)
