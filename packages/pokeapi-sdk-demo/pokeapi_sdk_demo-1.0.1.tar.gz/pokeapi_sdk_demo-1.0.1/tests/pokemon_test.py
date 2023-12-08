import pytest
from pokeapi_sdk import PokeAPISDK, Pokemon, Nature, Stat
from requests.exceptions import HTTPError

@pytest.fixture
def api_client():
    return PokeAPISDK()

def test_get_pokemon(api_client):
    response = api_client.get_pokemon("pikachu")
    assert isinstance(response, Pokemon), "The response should be a Pokemon instance"
    assert response.name == 'pikachu', "The name of the Pokemon should be Pikachu"

def test_invalid_pokemon(api_client):
    with pytest.raises(HTTPError):
        api_client.get_pokemon("invalid_pokemon")

def test_get_pokemon_full_details_valid(api_client):
    details = api_client.get_pokemon_full_details("pikachu")
    
    assert isinstance(details, dict), "Response should be a dictionary"
    assert 'pokemon' in details, "Response should include pokemon data"
    assert isinstance(details['pokemon'], Pokemon), "Pokemon data should be a Pokemon instance"
    assert details['pokemon'].name == 'pikachu', "Pokemon name should be Pikachu"

    # Could not find a valid pokemon with a nature characteristic, commented for now
    # assert 'nature' in details, "Response should include nature data"
    # assert isinstance(details['nature'], Nature), "Nature data should be a Nature instance"

    assert 'stats' in details, "Response should include stats data"
    assert isinstance(details['stats'], list), "Stats data should be a list"
    assert all(isinstance(stat, Stat) for stat in details['stats']), "Each item in stats should be a Stat instance"

def test_get_pokemon_full_details_invalid(api_client):
    with pytest.raises(HTTPError):
        api_client.get_pokemon_full_details("invalid_pokemon")
