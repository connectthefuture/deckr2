all: lint test
lint: autolint
	pylint --rcfile=config/pylintrc deckr tests
autolint:
	autopep8 -r --in-place deckr tests
test:
	../env/bin/nosetests -a '!integration'
integration:
	../env/bin/nosetests -a 'integration'
