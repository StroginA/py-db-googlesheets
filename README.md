# How to run 

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

## Links

Google Sheets: https://docs.google.com/spreadsheets/d/13tzDdsy5xPXmv-8Ew9OSM51vPl3Xlwo2Bz80XZxyry4/