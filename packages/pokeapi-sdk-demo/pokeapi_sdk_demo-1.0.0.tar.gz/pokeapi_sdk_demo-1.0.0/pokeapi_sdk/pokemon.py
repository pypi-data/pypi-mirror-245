class Pokemon:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.base_experience = data.get('base_experience')
        self.height = data.get('height')
        self.is_default = data.get('is_default')
        self.order = data.get('order')
        self.weight = data.get('weight')
        self.abilities = [_Ability(ability) for ability in data.get('abilities', [])]
        self.forms = [_NamedAPIResource(form) for form in data.get('forms', [])]
        self.game_indices = [_GameIndex(game_index) for game_index in data.get('game_indices', [])]
        self.held_items = [_HeldItem(item) for item in data.get('held_items', [])]
        self.location_area_encounters = data.get('location_area_encounters')
        self.moves = [_Move(move) for move in data.get('moves', [])]
        self.species = _NamedAPIResource(data.get('species'))
        self.stats = [_Stat(stat) for stat in data.get('stats', [])]
        self.types = [_Type(type_) for type_ in data.get('types', [])]
        self.sprites = _Sprites(data.get('sprites', {}))
        self.nature_url = self._extract_nature_url(data)
        self.stats_urls = self._extract_stats_urls(data)

    def _extract_nature_url(self, data):
        # Extract and return the nature URL from the data
        # Placeholder for actual implementation
        return data.get('nature', {}).get('url')

    def _extract_stats_urls(self, data):
        # Extract and return the list of stat URLs from the data
        # Placeholder for actual implementation
        return [stat['stat']['url'] for stat in data.get('stats', [])]

class _Ability:
    def __init__(self, data):
        self.is_hidden = data.get('is_hidden')
        self.slot = data.get('slot')
        self.ability = _NamedAPIResource(data.get('ability'))

class _NamedAPIResource:
    def __init__(self, data):
        self.name = data.get('name')
        self.url = data.get('url')

class _GameIndex:
    def __init__(self, data):
        self.game_index = data.get('game_index')
        self.version = _NamedAPIResource(data.get('version'))

class _HeldItem:
    def __init__(self, data):
        self.item = _NamedAPIResource(data.get('item'))
        self.version_details = [_VersionDetail(detail) for detail in data.get('version_details', [])]

class _VersionDetail:
    def __init__(self, data):
        self.rarity = data.get('rarity')
        self.version = _NamedAPIResource(data.get('version'))

class _Move:
    def __init__(self, data):
        self.move = _NamedAPIResource(data.get('move'))
        self.version_group_details = [_VersionGroupDetail(detail) for detail in data.get('version_group_details', [])]

class _VersionGroupDetail:
    def __init__(self, data):
        self.level_learned_at = data.get('level_learned_at')
        self.move_learn_method = _NamedAPIResource(data.get('move_learn_method'))
        self.version_group = _NamedAPIResource(data.get('version_group'))

class _Stat:
    def __init__(self, data):
        self.base_stat = data.get('base_stat')
        self.effort = data.get('effort')
        self.stat = _NamedAPIResource(data.get('stat'))

class _Type:
    def __init__(self, data):
        self.slot = data.get('slot')
        self.type = _NamedAPIResource(data.get('type'))

class _Sprites:
    def __init__(self, data):
        self.front_default = data.get('front_default')
        self.front_shiny = data.get('front_shiny')
        self.front_female = data.get('front_female')
        self.front_shiny_female = data.get('front_shiny_female')
        self.back_default = data.get('back_default')
        self.back_shiny = data.get('back_shiny')
        self.back_female = data.get('back_female')
        self.back_shiny_female = data.get('back_shiny_female')
        # Truncated for brevity
