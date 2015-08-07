
from game.game_object import GameObject
from game.zone import Zone


class Player(GameObject):

    def __init__(self):
        self.life = 20
        self.poison_counters = 0

	self.hand = Zone('hand', self)
	self.graveyard = Zone('graveyard', self)
	self.library = Zone('library', self)

    def play_card(self, card):
        pass

    def activate_ability(self, card, ability_index):
        pass

    def declare_attackers(self, attackers):
        pass

    def declare_defenders(self, defenders):
        pass

    def deal_combat_damage(self, comabt_damage):
        pass
        
    def pass_priority(self):
        pass
