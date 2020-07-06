install:
	pip install -r requirements.txt

start:
	FLASK_ENV=development FLASK_APP=tock.py flask run
