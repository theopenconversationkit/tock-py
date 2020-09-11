clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

bump-snapshot: clean-build
	bumpversion build;
	python setup.py sdist;
	twine upload dist/*

bump-release-major: clean-build
	bumpversion major;
	python setup.py sdist;
	twine upload dist/*

bump-release-minor: clean-build
	bumpversion major;
	python setup.py sdist;
	twine upload dist/*

bump-release-patch: clean-build
	bumpversion major;
	python setup.py sdist;
	twine upload dist/*

install:
	pip install -r requirements.txt

lint:
	flake8 ./tock