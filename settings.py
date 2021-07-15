from os import environ
from dotenv import load_dotenv

load_dotenv('.env')
API_TOKEN = environ['API_TOKEN']
CHANNEL_ID = environ['CHANNEL_ID']
EMAIL = environ['EMAIL']
EMAIL_PASSWORD = environ['EMAIL_PASSWORD']

