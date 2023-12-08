import requests
from .pokemon import Pokemon
from .nature import Nature
from .stat import Stat

class PokeAPISDK:
    BASE_URL = "https://pokeapi.co/api/v2/"

    def get_pokemon(self, identifier):
        data = self._get(f"pokemon/{identifier}")
        return Pokemon(data)

    def get_nature(self, identifier):
        data = self._get(f"nature/{identifier}")
        return Nature(data)

    def get_stat(self, identifier):
        data = self._get(f"stat/{identifier}")
        return Stat(data)
    
    def get_pokemon_full_details(self, identifier):
        """
        Fetches detailed information about a Pokemon including its nature and stats.
        
        :param identifier: Pokemon ID or name
        :return: A dictionary containing instances of Pokemon, Nature, and a list of Stat
        """
        # Fetch the basic Pokemon information
        pokemon_data = self._get(f"pokemon/{identifier}")
        pokemon = Pokemon(pokemon_data)

        # Fetch the nature information if available
        nature = None
        if pokemon.nature_url:
            nature_data = self._get(pokemon.nature_url)
            nature = Nature(nature_data)

        # Fetch stats information
        stats = []
        for stat_url in pokemon.stats_urls:
            stat_data = self._get(stat_url)
            stats.append(Stat(stat_data))

        # Combine all the data into a single dictionary
        return {
            "pokemon": pokemon,
            "nature": nature,
            "stats": stats
        }


    def _get(self, endpoint):
        # Check if the endpoint is already a complete URL
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            url = self.BASE_URL + endpoint

        response = requests.get(url)
        response.raise_for_status()
        return response.json()
