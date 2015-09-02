import lettuce_webdriver.django
import lettuce_webdriver.webdriver
from lettuce import *
from lettuce.django import django_url
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from nose.tools import *
from faker import Faker
from random import randrange
from webclient.models import *
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from time import sleep

fake = Faker()

def wait_for_connection(fn, time_waited=0):
    if time_waited > 5: return # We've waited for too long.
    get_socket_state_script = "return getSocketStateInEnglish()"
    socket_state = world.browser.execute_script(get_socket_state_script)
    if socket_state == "OPEN":
        return fn()
    else:
        sleep_time = 0.05
        sleep(sleep_time)
        return wait_for_connection(fn, time_waited=time_waited + sleep_time)

@before.all
def create_browser():
    capabilities = DesiredCapabilities.FIREFOX
    capabilities['loggingPrefs'] = { 'browser': 'ALL' }
    world.browser = webdriver.Firefox(capabilities=capabilities)

@after.all
def destroy_browser(results):
    world.browser.close()

@step(r'I visit the url "(.*)"')
def visit_url(step, url):
    full_url = django_url(url)
    world.browser.get(full_url)

@step(r'I create a standard game')
def create_standard_game(step):
    step.given('I fill in "name" with "{}"'.format(fake.word()))
    step.given('I fill in "variant" with "standard"')
    step.given('I fill in "max_players" with "{}"'.format(randrange(1, 8)))
    world.browser.find_element_by_class_name('create-game').click()
    world.game_id = world.browser.find_element_by_name('game_id').get_attribute('value')

@step(r'I join the game')
def join_game(step):
    world.nick = fake.name()
    step.given('I visit the url "{}"'.format("/staging/{}".format(world.game_id)))
    step.given('I fill in "nick" with "{}"'.format(world.nick))
    step.given('I press "Play"')

@step(r'I start the game')
def start_game(step):
    step.given('I press "Start Game"')

@step(r'I pass priority')
def pass_priorty(step):
    step.given('I press "Pass Priority"')

@step(r'I have created a standard game')
def have_created_standard_game(step):
    step.given('I visit the url "/game/create"')
    step.given('I create a standard game')

@step(r'I have joined a standard game')
def create_and_join_standard_game(step):
    step.given('I have created a standard game')
    step.given('I join the game')

@step(r'I have started a standard game')
def create_join_and_start_standard_game(step):
    step.given('I have joined a standard game')
    step.given('I start the game')

@step(r'I will be connected to the Deckr server')
def test_deckr_server_connection(step):
    expected_state = "OPEN"
    get_socket_state_script = "return getSocketStateInEnglish()"
    socket_state = wait_for_connection(
        lambda: world.browser.execute_script(get_socket_state_script))
    assert_equals(socket_state, expected_state)

@step(r'my game will be created')
def test_game_created(step):
    try:
        game = Game.objects.get(game_id=world.game_id)
    except ObjectDoesNotExist:
        game = None
    assert_is_not_none(game)
    game_id = world.browser.find_element_by_class_name('game-id').get_attribute('innerHTML')
    assert_equals(world.game_id, game_id)

@step(r'my game will appear in the lobby')
def test_game_in_lobby(step):
    step.given('I visit the url "/lobby"')
    world.browser.find_element_by_css_selector('tr[data-game-id="{}"]'.format(world.game_id))

@step(r'I will be in the game room')
def test_in_game_room(step):
    current_url = world.browser.current_url
    assert_in("game", current_url)
    assert_in(world.game_id, current_url)

@step(r'I will see my nickname')
def test_visible_nick(step):
    step.given('I see "{}"'.format(world.nick))

@step(r'the game will be started')
def test_is_game_started(step):
    # TODO: Check model for is_game_started
    start_game_btn = world.browser.find_element_by_class_name('start-game')
    assert_false(start_game_btn.is_displayed())

@step(r'I will no longer have priority')
def test_no_longer_have_priority(step):
    # TODO: Implement this test...
    pass
