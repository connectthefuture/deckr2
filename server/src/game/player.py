
from game.game_object import GameObject


class Player(GameObject):
    
    def __init__(self):
        self.life = 20
        self.poison_counters = 0

    def play_card(self, card):
        pass

    def activate_ability(self, card, ability_index):
        pass
