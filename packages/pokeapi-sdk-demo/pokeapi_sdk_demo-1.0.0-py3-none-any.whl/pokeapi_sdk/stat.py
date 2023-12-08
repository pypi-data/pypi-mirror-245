class Stat:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.is_battle_only = data.get('is_battle_only')
        self.game_index = data.get('game_index')
        self.move_damage_class = data.get('move_damage_class')
        self.affecting_moves = data.get('affecting_moves')
        self.affecting_natures = data.get('affecting_natures')
        self.characteristics = [_Characteristic(characteristic) for characteristic in data.get('characteristics', [])]

class _Characteristic:
    def __init__(self, data):
        self.url = data.get('url')
