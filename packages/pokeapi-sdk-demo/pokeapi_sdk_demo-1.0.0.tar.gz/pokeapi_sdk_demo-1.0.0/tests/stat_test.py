import pytest
from pokeapi_sdk import PokeAPISDK, Stat
from requests.exceptions import HTTPError

@pytest.fixture
def api_client():
    return PokeAPISDK()

def test_get_stat(api_client):
    response = api_client.get_stat(1)
    assert isinstance(response, Stat), "The response should be a Stat instance"
    assert response.name == 'hp', "The name of the Nature should be HP"

def test_invalid_stat(api_client):
    with pytest.raises(HTTPError):
        api_client.get_stat("unknown_stat")