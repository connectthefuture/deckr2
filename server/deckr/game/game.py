"""
This module provides code for the core game. Most of this is not logic, but instead simply a
container.
"""

import logging

import deckr.game.game_object
import deckr.game.player
import deckr.game.zone

LOGGER = logging.getLogger(__name__)


class CombatDamageManager(object):
    """
    Handles combat damage.
    """

    def __init__(self, game):
        self._game = game

    def deal_combat_damage(self):
        """
        Deals combat damage.
        """

        attackers = [x for x in self._game.battlefield if x.attacking]
        blockers = [x for x in self._game.battlefield if x.blocking]

        blocked = [x.blocking for x in blockers]
        unblocked = [x for x in attackers if x not in blocked]

        for attacker in unblocked:
            attacker.attacking.deal_combat_damage(attacker.power)

        for blocker in blockers:
            blocker.deal_combat_damage(blocker.blocking.power)
            blocker.blocking.deal_combat_damage(blocker.power)


class GameRegistry(object):
    """
    The game registry is responsible for handing out game_ids.
    """

    def __init__(self):
        self._game_objects = {}
        self._next_game_id = 0

    def register(self, game_object):
        """
        Register a new game_object and give it a game_id.

        Args:
            game_object GameObject: The object to register.
        """

        assert isinstance(game_object, deckr.game.game_object.GameObject)
        game_id = self._next_game_id
        game_object.game_id = game_id
        self._next_game_id += 1
        self._game_objects[game_id] = game_object

    def unregister(self, game_object):
        """
        Unregister a game_object.

        Args:
            game_object GameObject: The object to unregister.
        """

        assert game_object.game_id in self._game_objects
        del self._game_objects[game_object.game_id]

    def lookup(self, game_id):
        """
        Find a game object based on the ID.

        Args:
            game_id (int): The id to lookup.

        Returns:
            GameObject the game object with the corresponding ID.
        """

        return self._game_objects[game_id]

    def __getitem__(self, key):
        return self.lookup(key)

    def __iter__(self):
        return self._game_objects.values().__iter__()


class PlayerManager(object):
    """
    Manage players.
    """

    def __init__(self, game):
        self.players = []
        self._game = game

    def create_player(self, deck_list):
        """
        Create a new player and register it with this game.

        Returns:
            Player The newly created player
        """

        player = deckr.game.player.Player(self._game)

        self.players.append(player)
        # Register the player zones, mana pool, and cards
        self._game.registry.register(player)
        self._game.registry.register(player.hand)
        self._game.registry.register(player.library)
        self._game.registry.register(player.graveyard)
        self._game.registry.register(player.mana_pool)
        # Create the deck
        cards = self._game.card_library.create_from_list(deck_list)
        for card in cards:
            self._game.registry.register(card)
            player.library.append(card)
        return player

    def next_player(self, player):
        """
        Returns the next player in turn order.
        """

        assert player in self.players
        index = self.players.index(player)
        if index == len(self.players) - 1:
            return self.players[0]
        else:
            return self.players[index + 1]

    def start(self):
        """
        Start the game. Lock out any further players.
        """

        for player in self.players:
            player.start()

    def first_player(self):
        """
        Get the first player.
        """

        return self.players[0]

    def update_proto(self, proto):
        """
        Fill in player information into a gamestate proto.
        """

        for player in self.players:
            player_proto = proto.players.add()
            player.update_proto(player_proto)


class TurnManager(object):
    """
    Manage the turn (phase, priority player, etc.).
    """

    # Names for steps and phases
    UNTAP_STEP = 'untap'
    UPKEEP_STEP = 'upkeep'
    DRAW_STEP = 'draw'
    BEGIN_COMBAT_STEP = 'beginning of combat'
    DECLARE_ATTACKERS_STEP = 'declare attackers'
    DECLARE_BLOCKERS_STEP = 'declare blockers'
    COMBAT_DAMAGE_STEP = 'combat damage'
    END_OF_COMBAT_STEP = 'end of combat'
    END_STEP = 'end'
    CLEANUP_STEP = 'cleanup'

    BEGINNING_PHASE = 'beginning'
    PRECOMBAT_MAIN = 'precombat main'
    COMBAT_PHASE = 'combat'
    POSTCOMBAT_MAIN = 'postcombat main'
    END_PHASE = 'end'

    # An orderd list of step, phase tuples
    TURN_ORDER = [
        (UNTAP_STEP, BEGINNING_PHASE), (UPKEEP_STEP, BEGINNING_PHASE),
        (DRAW_STEP, BEGINNING_PHASE), (PRECOMBAT_MAIN, PRECOMBAT_MAIN),
        (BEGIN_COMBAT_STEP, COMBAT_PHASE),
        (DECLARE_ATTACKERS_STEP, COMBAT_PHASE),
        (DECLARE_BLOCKERS_STEP, COMBAT_PHASE),
        (COMBAT_DAMAGE_STEP, COMBAT_PHASE), (END_OF_COMBAT_STEP, COMBAT_PHASE),
        (POSTCOMBAT_MAIN, POSTCOMBAT_MAIN), (END_STEP, END_PHASE),
        (CLEANUP_STEP, END_PHASE)
    ]

    def __init__(self, game):
        self.step = None
        self.phase = None
        self.priority_player = None
        self.active_player = None
        self.turn = 0

        self._game = game

    def start(self):
        """
        Called to start the game.
        """

        self.step = 'upkeep'  # Nobody gets priority during untap; just skip it.
        self.phase = 'beginning'
        self.turn = 1
        self.active_player = self._game.player_manager.first_player()
        self.priority_player = self.active_player

    def advance(self):
        """
        Advance the turn. Either change priority, change step, change phase,
        or change active player (or all).
        """

        # Before anything we check state based actions

        next_player = self._game.player_manager.next_player(
            self.priority_player)
        if next_player == self.active_player:
            # Check the stack
            if self._game.stack.is_empty():
                self._next_step()
            else:
                self._game.stack.resolve()
                self.state_based_actions()
                self.priority_player = next_player
        else:
            self.state_based_actions()
            self.priority_player = next_player

    def _next_step(self):
        """
        Advance to the next step/phase. Run any turn based actions and give
        the active player priority.
        """

        step_phase = (self.step, self.phase)
        if step_phase == self.TURN_ORDER[-1]:
            self._next_turn()
        else:
            self.step, self.phase = self.TURN_ORDER[self.TURN_ORDER.index(
                step_phase) + 1]
        # First, we run an turn based actions
        self.turn_based_actions()
        self.state_based_actions()
        self.priority_player = self.active_player

    def _next_turn(self):
        """
        Go to the next turn.
        """

        self.active_player = self._game.player_manager.next_player(
            self.active_player)
        self.step, self.phase = self.TURN_ORDER[0]
        self.turn += 1
        for player in self._game.player_manager.players:
            player.start_new_turn()

    def turn_based_actions(self):
        """
        Run any turn based actions.
        """

        if self.step == self.DRAW_STEP:
            # Suppress the draw on the very first turn
            if (self.turn != 1 or self.active_player !=
                    self._game.player_manager.first_player()):
                self.active_player.draw()
        elif self.step == self.UNTAP_STEP:
            for card in self._game.battlefield:
                if card.tapped:
                    card.untap()
                card.has_summoning_sickness = False
        elif self.step == self.COMBAT_DAMAGE_STEP:
            self._game.combat_damage_manager.deal_combat_damage()

    def state_based_actions(self):
        """
        Check for state based actions.
        """

        self._game.state_based_action_manager.check()

    def update_proto(self, proto):
        """
        Update a proto with turn information.
        """

        proto.current_step = self.step
        proto.current_phase = self.phase
        proto.active_player = self.active_player.game_id
        proto.priority_player = self.priority_player.game_id


class StateBasedActionManager(object):
    """
    This manager handles all state based actions.
    """

    def __init__(self, game):
        self._game = game

    def check(self):
        """
        Check all state based actions. This is the main entry point into this
        class.
        """

        self._check_player_0_life()
        self._check_creature_damage()

    def _check_player_0_life(self):
        """
        Check for any players with 0 or less life.
        """

        for player in self._game.player_manager.players:
            if player.life <= 0:
                player.lost = True

    def _check_creature_damage(self):
        """
        Check any creatures for lethal damage.
        """

        for card in self._game.battlefield:
            print card.owner
            if card.is_creature() and card.damage >= card.toughness:
                self._game.battlefield.remove(card)
                card.owner.graveyard.append(card)


class MagicTheGathering(object):  # pylint: disable=too-many-instance-attributes
    """
    This is the actual game class. Really this should just coordinate conversation between
    various subclasses. Almost all of the logic should be kept out of this class.
    """

    def __init__(self, action_validator, card_library):
        # Objects inherited from the game_master
        self.action_validator = action_validator
        self.card_library = card_library

        # Local objects
        self.registry = GameRegistry()
        self.player_manager = PlayerManager(self)
        self.turn_manager = TurnManager(self)
        self.combat_damage_manager = CombatDamageManager(self)
        self.state_based_action_manager = StateBasedActionManager(self)

        # Each game has a set of shared zones
        self.battlefield = deckr.game.zone.Zone('battlefield', None)
        self.exile = deckr.game.zone.Zone('exile', None)
        self.stack = deckr.game.zone.Stack(name='stack', owner=None, game=self)

        # Register all game objects
        self.registry.register(self.battlefield)
        self.registry.register(self.exile)
        self.registry.register(self.stack)

        # Private bookkeeping
        self._started = False

    def start(self):
        """
        Start the game.
        """

        LOGGER.info("Starting game")
        self._started = True

        self.turn_manager.start()
        self.player_manager.start()

    def update_proto(self, proto):
        """
        Update a game state proto to reflect the current game state.
        """

        self.turn_manager.update_proto(proto)
        self.player_manager.update_proto(proto)
        self.stack.update_proto(proto.stack)
        self.battlefield.update_proto(proto.battlefield)
        self.exile.update_proto(proto.exile)
