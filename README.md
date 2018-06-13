# Item-Catalog-438

## ABOUT THE PROJECT :

This project is RESTful web application which accesses a PostgreSQL database to Catalog which will store information about   items and respective categories by using the Python framework Flask. Oauth2 authentication and authorization allows user to  perform CRUD (Create, Read, Update and Delete) operations. Therefore users who are successfully logged into Google accounts   can  perform these CRUD operations. 

## REPOSITORY : 

The project contains HTML files placed in templates folder , CSS files placed in static folder and consits of mainly 3 pthon files. 

1) To Create the SQL database.

2) To insert the items.  

3) To run the main program.

## REQUIREMENTS : 

* Python 2.7 or above  

* Vagrant

* Flask Framework 

* Oauth

* Requests

* SqlAlchemy 

## Local Development : 

* Go to project folder and open terminal emulator.

* Run ( sudo apt-get install python-vitualenv ).

* Run ( sudo apt-get install python-pip ).

* Run ( virtualenv flask-env ).

* Run ( source flask-env/bin/activate ).

* Run ( pip install sqlalchemy , pip install oauth2client, pip install requests, pip install dicttoxml ).

* Run the database_setup.py to create database.

* Run the populate_setup.py to insert items into databse.

* Run the helper.py to access new users.

* Run the project.py to connect to server. 

* Open the browser tab and type http://localhost:5000/ to run the project .

* By getting logged into google account we can perform the following CRUD operations.
