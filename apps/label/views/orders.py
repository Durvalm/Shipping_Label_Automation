from flask import Blueprint, request, render_template, redirect, url_for
import shippo
from apps.settings import SHIPPO_API_TOKEN, PARCEL, ADDRESS_FROM
from apps.models import db, User

shippo.config.api_key = SHIPPO_API_TOKEN
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    users = User.query.all()
    return render_template("dashboard.html", users=users)

@dashboard_bp.route("/order/<int:user_id>", methods=["GET"])
def order(user_id):
    user = User.query.get(user_id)
    return render_template("order.html", user=user)

@dashboard_bp.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_order(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route("/create_label/<int:user_id>", methods=["POST"])
def create_label(user_id):
    user = User.query.get(user_id)

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
    address_from = address_from,
    address_to = address_to,
    parcels = [parcel],
    is_async = False
    )

    # Makes sure the service used is USPS_PRIORITY
    usps_priority = ''
    for shipment_options in shipment.rates:
        if shipment_options["servicelevel"]["token"] == 'usps_priority':
            usps_priority = shipment_options
    
    # Store price
    user.price = usps_priority.amount
    user.rate = usps_priority.object_id
    db.session.commit()
 
    return redirect(url_for('dashboard.confirm_purchase', user_id=user.id))

@dashboard_bp.route("/confirm-purchase/<int:user_id>", methods=["GET","POST"])
def confirm_purchase(user_id):
    user = User.query.get(user_id)

    if request.method == "POST":
        transaction = shippo.Transaction.create(
            rate=user.rate,
            label_file_type="PDF"
        )
        # Confirm if transaction is successful
        if transaction.object_state == "VALID":
           print("SUCCESS")
           # Print Label

           # Delete order from DB
           db.session.delete(user)
           db.session.commit()           

        elif transaction.object_state == "INVALID":
            print('ERROR')
            # Send error message
        return redirect(url_for('dashboard.dashboard'))

    elif request.method == "GET":
        return render_template("confirm-purchase.html", user=user)
    




