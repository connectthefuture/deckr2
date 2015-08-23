from django.shortcuts import render

def index(request):
    """
    Return the home page without any context.
    """

    return render(request, "webclient/index.html", {})
