class Nature:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.decreased_stat = data.get('decreased_stat')
        self.increased_stat = data.get('increased_stat')
        self.hates_flavor = data.get('hates_flavor')
        self.likes_flavor = data.get('likes_flavor')
        self.move_battle_style_preferences = [_MoveBattleStylePreference(style) for style in data.get('move_battle_style_preferences', [])]

class _MoveBattleStylePreference:
    def __init__(self, data):
        self.high_hp_preference = data.get('high_hp_preference')
        self.low_hp_preference = data.get('low_hp_preference')
        self.move_battle_style = data.get('move_battle_style', {}).get('name')
