from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    variant = models.CharField(max_length=50)
    max_players = models.IntegerField()
    # created_by = models.ForeignKey(User)
    is_game_started = models.BooleanField(default=False)
    is_game_over = models.BooleanField(default=False)

    def __unicode__(self):
        """
        Unicode representation of a game.
        """

        return "{0}: {1}".format(self.game_id, self.name)
