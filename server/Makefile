all: lint all-tests
lint: format
	pylint --rcfile=config/pylintrc deckr tests || true
format:
	../env/bin/isort -y && autopep8 -r --in-place deckr tests --max-line-length 100
test:
	../env/bin/nosetests -a '!integration,!e2e'
integration:
	../env/bin/nosetests -a 'integration'
e2e:
	../env/bin/nosetests -a 'e2e'
all-tests:
	../env/bin/nosetests --with-coverage --cover-package=deckr --cover-branches
	coverage html
