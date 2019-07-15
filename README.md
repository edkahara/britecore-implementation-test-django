# Feature Request App

This is a feature request app. It allows IWS staff to view, create, update and delete feature requests. This project fulfills the
requirements listed on [PROJECT](https://github.com/edkahara/britecore-implementation-test/blob/master/PROJECT.md).

## How It Works

* Users can create feature requests by clicking on the NEW FEATURE REQUEST BUTTON.

* Users can update feature requests by clicking on the Edit button.

* Users can delete feature requests by clicking on the Delete button.

* Users can view the descriptions of their feature requests by clicking on the View button.

* Users can view all feature requests for each client sorted by priority on separate tables.

* Feature requests for each client cannot share priorities. When a created or updated request's priority is similar to that of an existing
request for a client, all of that client's priorities are re-ordered. This is done by incrementing each feature request that has a priority
greater than on equal to the new or updated request's priority by one.

## How To Run The Application Locally

### Clone this repository

  `git clone https://github.com/edkahara/britecore-implementation-test-django.git`

### Change directories into your repository

  `cd britecore-implementation-test-django`

### Create a virtual environment

  `python3 -m venv env` or `py -3 -m venv env` for Windows.

### Activate the virtual environment

  `source env/bin/activate` or `env\Scripts\activate` for Windows.

### Install the packages needed

  `pip install -r requirements.txt`

### Change directories into the feature_request project

  `cd feature_request`

### Make migrations

  `python manage.py makemigrations`

  `python manage.py migrate`

## Create an admin Users

  `python manage.py createsuperuser`

## Provide initial data for clients and products

  `manage.py loaddata clients.json products.json`

### Run the application

  `python manage.py runserver`

  Navigate to <http://localhost:8000> in your web browser to view the application.

## Tech Stack

* Ubuntu 18.04
* Python 3.6.7
* SQLite 3
* Django
* jQuery
* Materialize CSS

# Author

Edward Njoroge
