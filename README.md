# Planet

## Setting up locally

## Stack

- Python 3
- Virtualenv
- Flask


### Cloning the repository
```
git clone git@github.com:milktea/planet.git
```
Navigate to the app directory.
```
cd planet
```

### Creating and activating virtualenv
```
virtualenv -p python3 venv
virtualenv venv
. venv/bin/activate source
```

### Prerequisites
To install the project with all the requirements, run:
```
make init
```
or
```
pip install -r requirements.txt
```
Installing Flask and other dependencies


### Create the database
```
CREATE DATABASE planet;
CREATE DATABASE planet_test;
```
Running the instance later will automatically setup the database schema.

### Running the app
Configure your tunnel to forward to localhost:5000. To run the development server, run:
Export
```
export FLASK_APP=planet
export FLASK_ENV=development
```
Run the app
```
flask run
```
or
```
make serve
```
You should be able to access the application on this sample endpoint
http://localhost:5000/persons/1

### Importing people and company resources into the database

To import
```
flask db_seed
```
To drop data
```
flask db_drop
```


### Running the tests

Run the basic test suite with:
```
make test
```
or
```
pytest -v planet/tests/
```
#### For specific tests:

##### pytest -v <TEST_FILE_PATH> -k <NAME_OF_TEST>
```
e.g
pytest -v planet/tests/test_company.py -k test_add_company
```

# Endpoints
    Get company employees : /companies/<int:company_id>/employees

    Get person info: /persons/<int:person_id>

    Get 2 persons mutual friends: /persons/<int:person_id>/mutual_friends/<int:friend_id>


### Documentation



### Built With

* [Flask] - The web framework used
