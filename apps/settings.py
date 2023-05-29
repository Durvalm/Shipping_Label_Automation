import os
from dotenv import load_dotenv

if os.environ.get('FLASK_ENV') == 'development':
    env_file = '.env'
else:
    env_file = '.env.prod'
load_dotenv(env_file)


SECRET_KEY = os.environ.get("SECRET_KEY")

SHIPPO_API_TOKEN = os.environ.get("SHIPPO_TEST")

# DB
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///mydatabase.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Owner's info for "address from"
ADDRESS_FROM = {
    "name": os.environ.get("ADDRESS_FROM_NAME"),
    "street1": os.environ.get("ADDRESS_FROM_STREET1"),
    "street2": os.environ.get("ADDRESS_FROM_STREET2"),
    "city": os.environ.get("ADDRESS_FROM_CITY"),
    "state": os.environ.get("ADDRESS_FROM_STATE"),
    "zip": os.environ.get("ADDRESS_FROM_ZIP"),
    "country": os.environ.get("ADDRESS_FROM_COUNTRY"),
    }
 # Parcel standard info
PARCEL = {
        "length": "12.5",
        "width": "9.5",
        "height": "3",
        "distance_unit": "in",
        "weight": "1",
        "mass_unit": "lb",
}

