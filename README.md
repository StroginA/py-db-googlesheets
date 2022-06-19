# How to run 

## Python setup

Navigate to %project_directory% and run:

pip install virtualenv

virtualenv venv


Activate it by running /venv/Scripts/activate.bat

Run pip install -r requirements.txt


## Configuring the database

This project was set up on the DB cluster with English locale.

Install postgres, open the SQL shell, log in as the admin user and enter:

CREATE DATABASE ksdb;
CREATE USER ksuser WITH ENCRYPTED PASSWORD 'kspass';
ALTER ROLE ksuser SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE ksdb TO ksuser;

Navigate to %project_directory%/django_api and run:

python manage.py migrate db

## Script

Run python fetch_sheets.py

## Setting up the React app

From %project_directory% run npm install

## Django-React app

Setting

Navigate to %project_directory% and run npm start

## Links

Google Sheets: https://docs.google.com/spreadsheets/d/13tzDdsy5xPXmv-8Ew9OSM51vPl3Xlwo2Bz80XZxyry4/