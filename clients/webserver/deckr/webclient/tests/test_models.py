from django.test import TestCase
from random import randrange
from faker import Faker

from webclient.models import Game

fake = Faker()

def create_game(name=None):
    name = fake.word() if name is None else name
    return Game.objects.create(
        game_id=1,
        name=name,
        variant=fake.word(),
        max_players=randrange(2,8)
    )

class GameTestCase(TestCase):
    def setUp(self):
        self.name = fake.name()
        self.game = create_game(self.name)

    def test_string_representation(self):
        self.assertIn(self.name, self.game.__unicode__())
