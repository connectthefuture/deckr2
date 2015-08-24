from django.shortcuts import render

def index(request):
    """
    Return the home page without any context.
    """

    return render(request, "webclient/index.html", {})

def lobby(request):
    """
    Returns the lobby, where players can start, join, or watch games.
    """

    return render(request, "webclient/lobby.html", {})
