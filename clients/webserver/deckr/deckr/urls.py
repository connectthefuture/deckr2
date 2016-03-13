"""deckr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

INDEX = url(r'^$',
            'webclient.views.index',
            name='index')

LOBBY = url(r'^lobby/$',
            'webclient.views.lobby',
            name='lobby')

PROTO = url(r'^proto/(?P<base_file_name>.*)\.proto$',
            'webclient.views.proto',
            name='proto')

LOGIN = url(r'^login/$',
            'django.contrib.auth.views.login',
            {'template_name': 'auth/login.html'},
            name='login')

LOGOUT = url(r'^logout/$',
            'django.contrib.auth.views.logout',
            {'next_page': '/'},
            name='logout')

CREATE_GAME = url(r'^game/create$',
                 'webclient.views.create_game',
                 name='create_game')

STAGING = url(r'^staging/(?P<game_id>[0-9]+)$',
              'webclient.views.staging',
              name='staging')

GAME = url(r'^game/(?P<game_id>[0-9]+)$',
           'webclient.views.game',
           name='game')

urlpatterns = [
    INDEX,
    LOBBY,
    PROTO,
    # LOGIN,
    # LOGOUT,
    CREATE_GAME,
    STAGING,
    GAME,
    url(r'^admin/', include(admin.site.urls)),
]
