# Getting Started Instructions

# Using docker

Navigate to `/SOI_Server/soi_server` and run `docker-compose up --build` - that's it.
If you want to run the server in detached mode use `docker-compose up -d --build`.

# Set up a virtual environment

Another (more complicated) options is to create a virtual environment and install the requirements from `requirements.txt`.
This is the manuall way to set the project up which is not recommended!
You can ignore the following options when using docker!
## Set up the database

If you're python version less than 3.9 you have to follow these instructions to run sqlite:
https://code.djangoproject.com/wiki/JSON1Extension


After that naviagate to `/SOI_Server/soi_server` and execute the following commands in your virtual environment to set up the database:

`python manage.py makemigrations inspector`

`python manage.py migrate`

## Run the server on localhost

Then to start the server execute:

`python manage.py runserver`

The server should now be running at `http://localhost:8000`


## Run Unit Tests

To run the Unit tests for the database:

`python manage.py test inspector`

To run the Unit tests for the Pipline:
RUN IN THE soi_server DICTORNARY

`python -m unittest discover .\error_detection\`

