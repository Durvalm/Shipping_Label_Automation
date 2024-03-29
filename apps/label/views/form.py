from flask import Blueprint, request, render_template, redirect, flash, url_for
from apps.utils.alert import flash_message
import shippo
from apps.settings import SHIPPO_API_TOKEN, PARCEL, ADDRESS_FROM
from apps.models import db, User
from flask_login import login_required

shippo.config.api_key = SHIPPO_API_TOKEN
label_bp = Blueprint("/", __name__)

# Endpoints
@label_bp.route("/")
@login_required
def render_form():
    return render_template('index.html')

@label_bp.route("/submit", methods=['POST'])
def submit():
    """User submits shipping details form"""
    # Get data from form and fix the letter case
    address_data = {key: request.form[key].title() for key in ['name', 'country', 'street1', 'street2', 'state', 'city', 'zipcode']} 
    address_data['state'] = address_data['state'].upper()
    address_to = shippo.Address.create(**address_data, validate=True)

    # if address is valid, create user
    if address_to.validation_results.is_valid:
        user = User(**address_data)
        db.session.add(user)
        db.session.commit()

        flash_message("Created successfully.", "success")
        return redirect(url_for('dashboard.dashboard'))
    # if not, throw error
    else:
        flash_message("Address is not valid for shipping. Try again.", "warning")
        return redirect("/")
  
