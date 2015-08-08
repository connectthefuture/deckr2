all: lint test
lint: autolint
	pylint deckr tests
autolint:
	autopep8 -r --in-place deckr tests
test:
	nosetests tests
