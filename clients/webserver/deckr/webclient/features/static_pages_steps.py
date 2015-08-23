import lettuce_webdriver.django
import lettuce_webdriver.webdriver
from lettuce import *
from lettuce.django import django_url
from selenium import webdriver

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
