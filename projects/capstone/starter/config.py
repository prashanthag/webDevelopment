import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
database_name = "capstone"
#SQLALCHEMY_DATABASE_URI = 'postgres://postgres@localhost:5432/capstone'
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres','localhost:5432', database_name)
SQLALCHEMY_DATABASE_URI = database_path
SQLALCHEMY_TRACK_MODIFICATIONS=False
