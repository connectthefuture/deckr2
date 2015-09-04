from django import forms
from .models import Game

class CreateGameForm(forms.Form):
    """
    A form for creating games.
    """

    game_id = forms.IntegerField(widget=forms.HiddenInput, required=True)
    name = forms.CharField(required=True)
    variant = forms.CharField(required=True)
    max_players = forms.IntegerField(required=True)
    # private = forms.BooleanField(required=False)
