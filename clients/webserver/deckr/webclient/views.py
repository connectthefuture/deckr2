import os
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.templatetags.static import static
from django.http import HttpResponse
from django.conf import settings

from .forms import CreateGameForm
from .models import Game

def index(request):
    """
    Return the home page without any context.
    """

    return render(request, "webclient/index.html", {})

def lobby(request):
    """
    Returns the lobby, where players can start, join, or watch games.
    """
    games = list(Game.objects.filter())
    return render(request, "webclient/lobby.html", {
        'games': games,
    })

def create_game(request):
    """
    Returns the create game page where players can create a new game.
    """

    if request.method == "POST":
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game = Game.objects.create(
                game_id=form.cleaned_data['game_id'],
                name=form.cleaned_data['name'],
                variant=form.cleaned_data['variant'],
                max_players=form.cleaned_data['max_players'],
            )
            return redirect(reverse('staging', args=(game.game_id,)))
    else:
        form = CreateGameForm()

    return render(request, "game/create.html", {
        'form': form,
    })

def staging(request, game_id):
    """
    Returns the staging area for the given game_id.
    """

    game = get_object_or_404(Game, pk=game_id)

    return render(request, "game/staging.html", {
        'game': game,
    })

def game(request, game_id):
    """
    Returns the game room for the given game_id.
    """

    if request.method == "POST":
        request.session['is_player'] = request.POST.get('play', False)
        request.session['nick'] = request.POST.get("nick", "")

    game = get_object_or_404(Game, pk=game_id)

    return render(request, "game/room.html", {
        'game': game,
        'nick': request.session['nick'],
        'is_player': request.session['is_player'],
    })

def proto(request, base_file_name):
    """
    Returns appropriate .proto file.
    """

    proto_file = open(settings.PROTO_PATH + base_file_name + '.proto').read()
    return HttpResponse(proto_file, content_type='application/x-protobuf')
