"""
This module provides all of the code to test if actions are legal, and respond if they are not.
Note that the action validator is implemented as a service to allow for easier reloading.
"""

import deckr.core.service


class InvalidActionException(Exception):
    """
    This should be raised whenever a player tries to make an invalid action. It should include a
    descriptive reason why their action was invalid.
    """

    pass


class ActionValidator(deckr.core.service.Service):
    """
    Makes sure that actions are legal and if not gives a descriptive error message. Note that this
    is mostly stateless and so is reused across games.
    """

    def __init__(self, config=None):
        pass

    def start(self):
        """
        Run any setup for the validator.
        """

        pass

    def stop(self):
        """
        Run any teardown for the validator.
        """

        pass

    def validate(self, game, player, action, *args):
        """
        Validate a specific action. Returns if the action is valid, and raises an exception
        otherwise.

        Args:
            game MagicTheGathering: The game that the action is being applied to.
            action: String of the action being performed
        """

        if action == 'pass_priority':
            self._validate_pass_priority(game, player)
        elif action == 'play':
            self._validate_play(game, player, *args)
        elif action == 'activate':
            self._validate_activate(game, player, *args)
        elif action == 'declare_attackers':
            self._validate_declare_attackers(game, player, *args)
        elif action == 'declare_blockers':
            self._validate_declare_blockers(game, player, *args)
        else:
            raise ValueError("Invalid Action")

    def _validate_pass_priority(self, game, player):
        """
        Check if we can pass priority. The only real restriction is that we
        have priority.
        """

        has_priority(game, player)

    def _validate_play(self, game, player, card, mana_cost=None):
        """
        To play a card the following conditions need to be met:

        1) Has priority
        2) If it's a land
            a) Sorcery Speed
            b) Hsan't exceeded the land limit for the turn.
        """

        has_priority(game, player)

        if card.is_sorcery_speed():
            sorcery_speed(game, player)

        if card.is_land():
            land_limit(player)
        else:
            can_pay_mana_cost(player, card)
            ambigious_mana_cost(player, card, mana_cost)

    def _validate_activate(self, game, player, card, index):
        """
        Check that we can play an activated ability.
        """

        has_priority(game, player)
        can_pay_ability_cost(player, card, index)

    def _validate_declare_attackers(self, game, player, attackers):
        """
        Check the following:

        1) It's the active player
        2) It's the declare attackers step.
        3) All attackers are untaped.
        """

        is_active_player(game, player)
        is_step(game, 'declare attackers')
        are_untaped(attackers.keys())

    def _validate_declare_blockers(self, game, player, blockers):
        """
        Check the following:

        1) It's the declare blockers step.
        2) All blockers are untaped.
        """

        is_step(game, 'declare blockers')
        are_untaped(blockers.keys())

#################################
# Various rules checks go  here #
#################################


def check(error_string):
    """
    Checks the wrapped function, and if it returns a falsey value will raise
    an error with the specified string.
    """
    # pylint: disable=missing-docstring
    def wrapper(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            if not result:
                raise InvalidActionException(error_string)
        return inner
    return wrapper


@check("You need priority.")
def has_priority(game, player):
    """
    Does the player have priority?
    """

    return game.turn_manager.priority_player == player


@check("That can only be done at Sorcery speed")
def sorcery_speed(game, player):
    """
    Check that it is one of the main phases and that the stack is empty.
    """

    return (game.turn_manager.active_player == player and
            "main" in game.turn_manager.step and
            "main" in game.turn_manager.phase and game.stack.is_empty())


@check("You have played to many lands this turn")
def land_limit(player):
    """
    Check that a player hasn't played too many lands already.
    """

    return player.lands_played < player.land_limit


@check("You can't pay the mana cost for that card")
def can_pay_mana_cost(player, card):
    """
    Check that a player can pay the mana cost for a card.
    """

    return player.mana_pool.can_pay(card.mana_cost)

@check("You need to specify how you want to pay the mana cost; it's ambigious")
def ambigious_mana_cost(player, card, mana_cost):
    """
    Under the assumption that we can pay, see if we can pay exactly or if
    it's ambigious. If it's ambigious look at the mana_cost passed in and make
    sure that it's equivalent to the mana cost on the card.
    """

    return player.mana_pool.can_pay_exact(card.mana_cost)


@check("You can't pay the cost for that ability")
def can_pay_ability_cost(player, card, index):
    """
    Check that we can pay the cost for an activated ability.
    """

    return card.abilities[index].can_pay_cost(player)


@check("You can't do that during this step")
def is_step(game, step):
    """
    Check that the game is in the proper step.
    """

    return game.turn_manager.step == step


@check("All creatures must be untapped to do that")
def are_untaped(creatures):
    """
    Make sure that every creature is untapped.
    """

    return all(not x.tapped for x in creatures)


@check("Only the active player can do that right now")
def is_active_player(game, player):
    """
    Make sure that the player is the active player.
    """

    print game.turn_manager.active_player, player
    return game.turn_manager.active_player == player
