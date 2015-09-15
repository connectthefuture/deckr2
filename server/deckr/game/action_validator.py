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
        else:
            raise ValueError("Invalid Action")

    def _validate_pass_priority(self, game, player):
        """
        Check if we can pass priority. The only real restriction is that we
        have priority.
        """

        has_priority(game, player)

    def _validate_play(self, game, player, card):
        """
        To play a card the following conditions need to be met:

        1) Has priority
        2) If it's a land
            a) Sorcery Speed
            b) Hsan't exceeded the land limit for the turn.
        """

        has_priority(game, player)

        if card.is_land():
            sorcery_speed(game)
            land_limit(player)
        else:
            pass

#################################
# Various rules checks go  here #
#################################


def check(error_string):
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
def sorcery_speed(game):
    """
    Check that it is one of the main phases and that the stack is empty.
    """

    return ("main" in game.turn_manager.step and
            "main" in game.turn_manager.phase and
            game.stack.is_empty())


@check("You have played to many lands this turn")
def land_limit(player):
    """
    Check that a player hasn't played too many lands already.
    """

    return player.lands_played < player.land_limit
