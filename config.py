import os
from dotenv import find_dotenv, load_dotenv

# this finds the .env file and loads all the vars as env vars!
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# now instead of having to access the env var directly when we need to anywhere in the app, 
# we can enumerate those vars here then process them into app.config
SECRET_KEY = os.getenv('SECRET_KEY')
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')

SQUARE_ACCESS_TOKEN = os.getenv('SQUARE_ACCESS_TOKEN')
SQUARE_LOCATION_ID = os.getenv('SQUARE_LOCATION_ID')



# We can also config with classes!
# class Config:
#     """Base config."""
#     SECRET_KEY = os.getenv('SECRET_KEY')


# class ProdConfig(Config):
#     """Production config."""
#     DB_HOST = os.getenv("PROD_DB_HOST")
#     DB_USERNAME = os.getenv("PROD_DB_USERNAME")
#     DB_PASSWORD = os.getenv("PROD_DB_PASSWORD")
#     DB_DATABASE = os.getenv("PROD_DB_DATABASE")


# class DevConfig(Config):
#     """Development config."""
#     DB_HOST = os.getenv("DB_HOST")
#     DB_USERNAME = os.getenv("DB_USERNAME")
#     DB_PASSWORD = os.getenv("DB_PASSWORD")
#     DB_DATABASE = os.getenv("DB_DATABASE")
