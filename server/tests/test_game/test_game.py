"""
This contains all of the tests directly related to the MagicTheGathering game and it's assocaited
classes.
"""

import unittest

import deckr.game.card
import deckr.game.game
import deckr.game.game_object
import deckr.game.player
import mock
import proto.game_pb2 as game_proto


class CombatDamageManagerTestCase(unittest.TestCase):
    """
    Test the combat damage manager.
    """

    def setUp(self):
        self.game = mock.MagicMock()
        self.player = mock.MagicMock()
        self.attacker = deckr.game.card.Card()
        self.blocker = deckr.game.card.Card()
        self.attacker.power = 2
        self.blocker.power = 2
        self.attacker.deal_combat_damage = mock.MagicMock()
        self.blocker.deal_combat_damage = mock.MagicMock()
        self.game.battlefield = [self.attacker, self.blocker]
        self.attacker.attacking = self.player
        self.combat_damage_manager = deckr.game.game.CombatDamageManager(
            self.game)

    def test_single_attacker(self):
        """
        Make sure that we can have a single attacker deal combat damage to a player.
        """


        self.combat_damage_manager.deal_combat_damage()
        self.player.deal_combat_damage.assert_called_with(2)

    def test_blocker(self):
        """
        Make sure we can have an attacker and a single blocker.
        """

        self.blocker.blocking = self.attacker
        self.combat_damage_manager.deal_combat_damage()
        self.player.deal_combat_damage.assert_not_called()
        self.blocker.deal_combat_damage.assert_called_with(2)
        self.attacker.deal_combat_damage.assert_called_with(2)


class PlayerManagerTestCase(unittest.TestCase):
    """
    Test the player manager.
    """

    def setUp(self):
        self.game = mock.MagicMock()
        self.player_manager = deckr.game.game.PlayerManager(self.game)

    def assert_registered(self, obj):
        """
        Assert that an object was registered with the game.
        """

        self.game.registry.register.assert_any_call(obj)

    def test_create_player(self):
        """
        Make sure we can create a player. It should be registered with the game.
        """

        player = self.player_manager.create_player([])
        self.assertIsNotNone(player)
        self.assertTrue(isinstance(player, deckr.game.player.Player))
        self.assertIn(player, self.player_manager.players)
        self.assert_registered(player)
        self.assert_registered(player.hand)
        self.assert_registered(player.library)
        self.assert_registered(player.graveyard)
        self.assert_registered(player.mana_pool)

    def test_create_player_deck(self):
        """
        Make sure we can create a player and their deck.
        """

        card = deckr.game.game_object.GameObject()
        self.game.card_library.create_from_list.return_value = [card]
        player = self.player_manager.create_player(["Forest"])
        self.assertIn(card, player.library)
        self.assert_registered(card)

    def test_start(self):
        """
        Make sure we properly start each player.
        """

        player = self.player_manager.create_player([])
        player.start = mock.MagicMock()
        self.player_manager.start()
        player.start.assert_called_with()


class TurnManagerTestCase(unittest.TestCase):
    """
    Test the turn manager.
    """

    def setUp(self):
        self.game = mock.MagicMock()
        self.player1 = mock.MagicMock()
        self.player2 = mock.MagicMock()

        self.turn_manager = deckr.game.game.TurnManager(self.game)

        def fake_next_player(player):
            """Fake call to next player."""
            return self.player2 if player == self.player1 else self.player1

        self.game.player_manager.next_player.side_effect = fake_next_player

        self.turn_manager.phase = 'beginning'
        self.turn_manager.step = 'upkeep'
        self.turn_manager.active_player = self.player1
        self.turn_manager.priority_player = self.player1
        self.turn_manager.turn = 1

    def assert_turn_state(self, step, phase, active, priority):
        """
        Assert on the step, phase, active and priority players.
        """

        self.assertEqual(self.turn_manager.step, step)
        self.assertEqual(self.turn_manager.phase, phase)
        self.assertEqual(self.turn_manager.active_player, active)
        self.assertEqual(self.turn_manager.priority_player, priority)

    def test_full_turn(self):
        """
        Test a full turn.
        """

        turns = deckr.game.game.TurnManager
        # Suppress turn based actions
        self.turn_manager.turn_based_actions = lambda: None
        self.turn_manager.advance()
        self.assert_turn_state(turns.UPKEEP_STEP, turns.BEGINNING_PHASE,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.DRAW_STEP, turns.BEGINNING_PHASE,
                               self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.DRAW_STEP, turns.BEGINNING_PHASE,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.PRECOMBAT_MAIN, turns.PRECOMBAT_MAIN,
                               self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.PRECOMBAT_MAIN, turns.PRECOMBAT_MAIN,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.BEGIN_COMBAT_STEP, turns.COMBAT_PHASE,
                               self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.BEGIN_COMBAT_STEP, turns.COMBAT_PHASE,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.DECLARE_ATTACKERS_STEP,
                               turns.COMBAT_PHASE, self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.DECLARE_ATTACKERS_STEP,
                               turns.COMBAT_PHASE, self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.DECLARE_BLOCKERS_STEP, turns.COMBAT_PHASE,
                               self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.DECLARE_BLOCKERS_STEP, turns.COMBAT_PHASE,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.COMBAT_DAMAGE_STEP, turns.COMBAT_PHASE,
                               self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.COMBAT_DAMAGE_STEP, turns.COMBAT_PHASE,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.END_OF_COMBAT_STEP, turns.COMBAT_PHASE,
                               self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.END_OF_COMBAT_STEP, turns.COMBAT_PHASE,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.POSTCOMBAT_MAIN, turns.POSTCOMBAT_MAIN,
                               self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.POSTCOMBAT_MAIN, turns.POSTCOMBAT_MAIN,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.END_STEP, turns.END_PHASE, self.player1,
                               self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.END_STEP, turns.END_PHASE, self.player1,
                               self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.CLEANUP_STEP, turns.END_PHASE,
                               self.player1, self.player1)
        self.turn_manager.advance()
        self.assert_turn_state(turns.CLEANUP_STEP, turns.END_PHASE,
                               self.player1, self.player2)
        self.turn_manager.advance()
        self.assert_turn_state(turns.UNTAP_STEP, turns.BEGINNING_PHASE,
                               self.player2, self.player2)
        self.assertEqual(self.turn_manager.turn, 2)

    def test_draw_action(self):
        """
        Make sure at the start of the draw step we actually draw a card.
        """

        self.turn_manager.step = self.turn_manager.DRAW_STEP
        self.turn_manager.phase = self.turn_manager.BEGINNING_PHASE

        # Make sure we suppress if first player, first turn
        self.turn_manager.turn = 1
        self.game.player_manager.first_player.return_value = self.player1

        self.turn_manager.turn_based_actions()
        self.player1.draw.assert_not_called()

        # Make sure we actually draw otherwise
        self.turn_manager.turn = 2
        self.turn_manager.turn_based_actions()
        self.player1.draw.assert_called_with()

    def test_deal_combat_damage(self):
        """
        Make sure that we deal combat damage during the combat damage phase.
        """

        self.turn_manager.step = self.turn_manager.COMBAT_DAMAGE_STEP
        self.turn_manager.phase = self.turn_manager.COMBAT_PHASE
        self.turn_manager.turn_based_actions()
        self.game.combat_damage_manager.deal_combat_damage.assert_called_with()

    def test_resolve_stack(self):
        """
        Make sure we don't continue if the stack isn't empty.
        """

        self.game.stack.is_empty.return_value = False
        self.turn_manager.turn_based_actions = lambda: None
        self.turn_manager.advance()
        self.turn_manager.advance()
        # We should still be in the default step/phase
        self.assert_turn_state(deckr.game.game.TurnManager.UPKEEP_STEP,
                               deckr.game.game.TurnManager.BEGINNING_PHASE,
                               self.player1, self.player1)
        self.game.stack.resolve.assert_called_with()


class MagicTheGatheringTestCase(unittest.TestCase):
    """
    Test the core game logic
    """

    def setUp(self):
        self.mock_action_validator = mock.MagicMock()
        self.card_library = mock.MagicMock()
        self.game = deckr.game.game.MagicTheGathering(
            self.mock_action_validator, self.card_library)

    def test_update_proto(self):
        """
        Make sure that we properly update the game state proto.
        """

        player1 = mock.MagicMock()
        player1.game_id = 1
        proto = game_proto.GameState()
        mock_game_object = deckr.game.game_object.GameObject()
        mock_game_object.update_proto = mock.MagicMock()

        # Set up the game
        self.game.turn_manager.step = 'untap'
        self.game.turn_manager.phase = 'beginning'
        self.game.turn_manager.active_player = player1
        self.game.turn_manager.priority_player = player1
        self.game.player_manager.players = [player1]

        self.game.update_proto(proto)
        self.assertEqual(proto.current_step, 'untap')
        self.assertEqual(proto.current_phase, 'beginning')
        self.assertEqual(len(proto.players), 1)

        self.assertEqual(player1.update_proto.call_count, 1)


class GameRegistryTestCase(unittest.TestCase):
    """
    Tests directly related to the game registry.
    """

    def setUp(self):
        self.game_object1 = deckr.game.game_object.GameObject()
        self.game_object2 = deckr.game.game_object.GameObject()
        self.registry = deckr.game.game.GameRegistry()

    def test_register(self):
        """
        Test the register function. It should assign a unique game_id to each game object.
        """

        self.registry.register(self.game_object1)
        self.registry.register(self.game_object2)
        self.assertIsNotNone(self.game_object1.game_id)
        self.assertIsNotNone(self.game_object2.game_id)
        self.assertNotEqual(self.game_object1.game_id,
                            self.game_object2.game_id)

    def test_lookup(self):
        """
        Make sure we can lookup a game object by ID
        """

        self.registry.register(self.game_object1)
        self.assertEqual(self.registry.lookup(
            self.game_object1.game_id), self.game_object1)

    def test_unregister(self):
        """
        Make sure we can unregister an object.
        """

        self.registry.register(self.game_object1)
        self.registry.unregister(self.game_object1)
        self.assertRaises(KeyError, self.registry.lookup,
                          self.game_object1.game_id)
