import os
from django.shortcuts import render
from django.templatetags.static import static
from django.http import HttpResponse
from django.conf import settings

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

def proto(request, base_file_name):
    """
    Returns appropriate .proto file.
    """

    proto_file = open(settings.PROTO_PATH + base_file_name + '.proto').read()
    return HttpResponse(proto_file, content_type='application/x-protobuf')
