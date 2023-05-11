from flask import Blueprint, request, render_template
import shippo
from apps.settings import SHIPPO_API_TOKEN, PARCEL, ADDRESS_FROM

shippo.config.api_key = SHIPPO_API_TOKEN
label_bp = Blueprint('/', __name__)

# Endpoints
@label_bp.route("/")
def render_form():
    return render_template('index.html')

@label_bp.route("/submit", methods=['POST'])
def submit():
    """Test access to form"""
    name = request.form['name']
    country = request.form['country']
    street1 = request.form['street1']
    street2 = request.form['street2']
    state = request.form['state']
    city = request.form['city']
    zipcode = request.form['zipcode']

    address_from = ADDRESS_FROM
    parcel = PARCEL
    address_to = {
        "name": name,
        "street1": street1,
        "street2": street2,
        "city": city,
        "state": state,
        "zip": zipcode,
        "country": country,
    }

    shipment = shippo.Shipment.create(
    address_from = address_from,
    address_to = address_to,
    parcels = [parcel],
    create_shipping_label=False,
    is_async = False
    )

    usps_priority = ''
    for shipment_options in shipment.rates:
        if shipment_options["servicelevel"]["token"] == 'usps_priority':
            usps_priority = shipment_options


    transaction = shippo.Transaction.create(
        rate=usps_priority.object_id,
        label_file_type="PDF",
        create_shipping_label=False
    )
  
    print(transaction)
    # Do something with the data
    return f"Success"

