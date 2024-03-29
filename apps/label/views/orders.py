from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required
import shippo
from apps.utils.alert import flash_message
from apps.settings import SHIPPO_API_TOKEN, PARCEL, ADDRESS_FROM
from apps.models import db, User
import requests

import time


shippo.config.api_key = SHIPPO_API_TOKEN
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    users = User.query.filter_by(is_completed=False).order_by(User.created_at.desc()).all()
    return render_template("dashboard/dashboard.html", users=users)

@dashboard_bp.route("/order/<int:user_id>", methods=["GET"])
@login_required
def order(user_id):
    user = User.query.get(user_id)
    return render_template("dashboard/order.html", user=user)

@dashboard_bp.route("/delete/<int:user_id>", methods=["DELETE", "GET"])
@login_required
def delete_order(user_id):
    """if label was purchased, set to complete, if not, delete from DB"""
    user = User.query.get(user_id)
    if user.label_url:
        user.is_completed = True
    else:
        db.session.delete(user)
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route("/create_label/<int:user_id>", methods=["POST"])
@login_required
def create_label(user_id):
    """Creates the Shipping object collecting information such as ADDRESS_FROM, ADDRESS_TO,
    PARCEL, etc, and also stores the rate and price of shipping, we'll use this informatiom
    in the next step to complete the transaction. """
    # Update Address
    address_data = {key: request.form[key] for key in ['name', 'country', 'street1', 'street2', 'state', 'city', 'zipcode']}
    user = User.query.get(user_id)
    for key, value in address_data.items():
        setattr(user, key, value)
    db.session.commit()

    shipment = create_shipping(user)
    create_shipping_service(user, shipment)
     
 
    return redirect(url_for('dashboard.confirm_purchase', user_id=user.id))

@dashboard_bp.route("/confirm-purchase/<int:user_id>", methods=["GET","POST"])
@login_required
def confirm_purchase(user_id):
    """This endpoint buys the label and makes it available to be printed
    in Shippo's website, the next step is to print automatically."""
    user = User.query.get(user_id)

    if request.method == "POST":
        transaction = shippo.Transaction.create(
            rate=user.rate,
            is_async=False,
            label_file_type="PDF_4x6",
        )
        # Confirm if transaction is successful
        if transaction.object_state == "VALID":
            # Success message
            flash_message("Label was successfully created.", "success")   
            return redirect(url_for('dashboard.retrieve_label', id=transaction.object_id, user_id=user_id))        

        elif transaction.object_state == "INVALID":
            # Send error message
            flash_message("There is an error with the address. Try again.", "error")
        return redirect(url_for('dashboard.dashboard'))


    elif request.method == "GET":
        return render_template("dashboard/confirm-purchase.html", user=user)


@dashboard_bp.route("/retrieve-label/<string:id>/<string:user_id>", methods=["GET"])
@login_required
def retrieve_label(id, user_id):
    """Retrieves the label url and adds to the DB"""
    time.sleep(3)
    transaction = shippo.Transaction.retrieve(object_id=id)
    label_url = transaction.label_url

    # Add to the DB
    user = User.query.get(user_id)
    user.label_url = label_url
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))

def create_shipping(user):
    # Shipping information
    address_from = ADDRESS_FROM
    parcel = PARCEL
    address_to = {
        "name": user.name,
        "street1": user.street1,
        "street2": user.street2,
        "city": user.city,
        "state": user.state,
        "zip": user.zipcode,
        "country": user.country,
    }
     # Creates Shipping
    shipment = shippo.Shipment.create(
    address_from=address_from,
    address_to=address_to,
    object_purpose="PURCHASE",
    parcels=[parcel],
    is_async=False
    )
    return shipment

def create_shipping_service(user, shipment):
 # Makes sure the service used is USPS_PRIORITY
    usps_priority = ''
    for shipment_options in shipment.rates:
        if shipment_options["servicelevel"]["token"] == 'usps_priority':
            usps_priority = shipment_options
    
    # Store price
    user.price = usps_priority.amount
    user.rate = usps_priority.object_id
    db.session.commit()

