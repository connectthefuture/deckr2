all: lint test integration
lint: format
	pylint --rcfile=config/pylintrc deckr tests || true
format:
	autopep8 -r --in-place deckr tests --max-line-length 100
test:
	../env/bin/nosetests -a '!integration' --with-coverage --cover-package=deckr --cover-branches
	coverage html
test-no-cover:
	../env/bin/nosetests -a '!integration'
integration:
	../env/bin/nosetests -a 'integration'
