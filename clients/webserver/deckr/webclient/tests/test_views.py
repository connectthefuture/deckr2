from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from random import randrange
from faker import Faker

import webclient.views
from webclient.models import Game
from webclient.tests.test_models import create_game

fake = Faker()

def set_session_vars(client, session_vars):
    for key, value in session_vars.iteritems():
        client.session[key] = value
    client.session.save()

class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_accesible(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class LobbyTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_accesible(self):
        response = self.client.get(reverse('lobby'))
        self.assertEqual(response.status_code, 200)

class CreateGameTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_accesible(self):
        response = self.client.get(reverse('create_game'))
        self.assertEqual(response.status_code, 200)

    def test_create_game_form_valid_data(self):
        form_data = {
            'game_id': 1,
            'name': fake.name(),
            'variant': fake.word(),
            'max_players': randrange(2,8),
        }
        response = self.client.post(reverse('create_game'), form_data)
        game = list(Game.objects.all())[-1]

        self.assertTrue(Game.objects.all().count() > 0)
        self.assertRedirects(response, reverse('staging', args=(game.game_id,)))

    def test_create_game_form_invalid_data(self):
        response = self.client.post(reverse('create_game'), {})
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.assertFormError(response, 'form', 'game_id', 'This field is required.')
        self.assertFormError(response, 'form', 'variant', 'This field is required.')
        self.assertFormError(response, 'form', 'max_players', 'This field is required.')

class StagingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.game = create_game()

    def test_accesible(self):
        response = self.client.get(reverse('staging', args=(self.game.game_id,)))
        self.assertEqual(response.status_code, 200)

    def test_join_as_player(self):
        form_data = {
            'play': 1,
            'nick': fake.name()
        }
        response = self.client.post(reverse('game', args=(self.game.game_id,)), form_data)
        self.assertEqual(self.client.session['nick'], form_data['nick'])
        self.assertEqual(self.client.session['client_type'], 'PLAYER')

    def test_join_as_spectator(self):
        pass # TODO: Implement spectators.

class GameRoomTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.game = create_game()

        set_session_vars(self.client, {
            'nick': fake.name(),
            'client_type': 'PLAYER'}
        )

    def test_accesible(self):
        response = self.client.post(reverse('game', args=(self.game.game_id,)))
        self.assertEqual(response.status_code, 200)

class ProtoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_accesible(self):
        response = self.client.get(reverse('proto', args=('client_message',)))
        self.assertEqual(response.status_code, 200)
