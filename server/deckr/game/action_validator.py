"""
This module provides all of the code to test if actions are legal, and respond if they are not.
Note that the action validator is implemented as a service to allow for easier reloading.
"""

import deckr.services.service


class InvalidActionException(Exception):
    """
    This should be raised whenever a player tries to make an invalid action. It should include a
    descriptive reason why their action was invalid.
    """

    pass


class ActionValidator(deckr.services.service.Service):
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

    def validate(self, game, action):
        """
        Validate a specific action. Returns if the action is valid, and raises an exception
        otherwise.

        Args:
            game MagicTheGathering: The game that the action is being applied to.
            action (???): An action that is being performed.
        """

        pass
