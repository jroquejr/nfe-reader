# nfe-reader
API to read data from NFE coupon.

* Read from qrcode url
* Read by code


## For run the project

1. Create a virtualenv `pipenv --python 3.7.3`
2. Load the virtualenv `pipenv shell`
3. Install the dependencies (dev too)  `pipenv install --dev`

# Important commands

1. Run automatic code format and sort imports: `make format`
2. Run the *tests*: `make test`
3. Check the tests coverage with html report: `make coverage`
4. Run local crawler (only BA for that moment): `python local_run.py --url <URL>`
5. Run the API locally: `python run.py`
6. Run the API using flask on Docker: `docker-compose up -d api-flask`
7. Run the API using gunicorn on Docker: `docker-compose up -d api-gunicorn`
8. Run the command line crawler inside Docker: `docker-compose run crawler -h <URL>`
