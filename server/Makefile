all: lint test
lint: format
	pylint --rcfile=config/pylintrc deckr tests
format:
	autopep8 -r --in-place deckr tests --max-line-length 100
test:
	../env/bin/nosetests -a '!integration' --with-coverage --cover-package=deckr --cover-branches
	coverage html
test-no-cover:
	../env/bin/nosetests -a '!integration'
integration:
	../env/bin/nosetests -a 'integration'
