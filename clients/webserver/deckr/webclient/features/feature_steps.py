import lettuce_webdriver.django
import lettuce_webdriver.webdriver
from lettuce import *
from lettuce.django import django_url
from selenium import webdriver
from nose.tools import *

@before.all
def create_browser():
    world.browser = webdriver.PhantomJS()

@after.all
def destroy_browser(results):
    world.browser.close()

@step(r'I visit the url "(.*)"')
def visit_url(step, url):
    full_url = django_url(url)
    world.browser.get(full_url)

@step(r'I will be connected to the Deckr server')
def test_deckr_server_connection(step):
    expected_state = "OPEN"
    get_socket_state_script = "return getSocketStateInEnglish()"
    socket_state = world.browser.execute_script(get_socket_state_script)
    # This will randomly fail when sockjs takes a while to connect.
    # This can probably be fixed by waiting for some element to appear on
    # the page before executing the script.
    assert_equals(socket_state, expected_state)
