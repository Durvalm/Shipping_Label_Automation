from flask import Blueprint, request, render_template, redirect, flash
from apps.utils.alert import flash_message
import shippo
from apps.settings import SHIPPO_API_TOKEN, PARCEL, ADDRESS_FROM
from apps.models import db, User

shippo.config.api_key = SHIPPO_API_TOKEN
label_bp = Blueprint("/", __name__)

# Endpoints
@label_bp.route("/")
def render_form():
    return render_template('index.html')

@label_bp.route("/submit", methods=['POST'])
def submit():
    """User submits shipping details form"""
    address_data = {key: request.form[key] for key in ['name', 'country', 'street1', 'street2', 'state', 'city', 'zipcode']}
    address_to = shippo.Address.create(**address_data, validate=True)

    # if address is valid, create user
    if address_to.validation_results.is_valid:
        user = User(**address_data)
        db.session.add(user)
        db.session.commit()
        return render_template('success.html')
    # if not, throw error
    else:
        flash_message("Address is not valid for shipping. Try again.", "warning")
        return redirect("/")
  
