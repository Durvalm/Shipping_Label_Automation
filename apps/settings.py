from os import environ

SHIPPO_API_TOKEN = environ.get("SHIPPO_TEST")

# DB
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///mydatabase.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Owner's info for "address from"
ADDRESS_FROM = {
    "name": environ.get("ADDRESS_FROM_NAME"),
    "street1": environ.get("ADDRESS_FROM_STREET1"),
    "street2": environ.get("ADDRESS_FROM_STREET2"),
    "city": environ.get("ADDRESS_FROM_CITY"),
    "state": environ.get("ADDRESS_FROM_STATE"),
    "zip": environ.get("ADDRESS_FROM_ZIP"),
    "country": environ.get("ADDRESS_FROM_COUNTRY"),
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