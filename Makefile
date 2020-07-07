clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

install:
	pip install -r requirements.txt

lint:
	flake8 ./tock