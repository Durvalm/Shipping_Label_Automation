from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required
import shippo
from apps.utils.alert import flash_message
from apps.settings import SHIPPO_API_TOKEN, PARCEL, ADDRESS_FROM
from apps.models import db, User

# For printing functionality
import time
import requests
import tempfile
import subprocess
import os

shippo.config.api_key = SHIPPO_API_TOKEN
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    users = User.query.filter_by(is_completed=False).all()
    return render_template("dashboard.html", users=users)

@dashboard_bp.route("/order/<int:user_id>", methods=["GET"])
@login_required
def order(user_id):
    user = User.query.get(user_id)
    return render_template("order.html", user=user)

@dashboard_bp.route("/delete/<int:user_id>", methods=["DELETE", "GET"])
@login_required
def delete_order(user_id):
    user = User.query.get(user_id)
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
            # Delete order from DB
            user.is_completed = True
            db.session.commit()
            # Success message
            flash_message("Label was successfully created.", "success")           

        elif transaction.object_state == "INVALID":
            # Send error message
            flash_message("There is an error with the address. Try again.", "error")
        return redirect(url_for('dashboard.dashboard'))
        # return redirect(url_for('dashboard.print_label', id=transaction.object_id))


    elif request.method == "GET":
        return render_template("confirm-purchase.html", user=user)


# @dashboard_bp.route("/print-label/<string:id>", methods=["GET"])
# def print_label(id):
#     time.sleep(2)
#     transaction = shippo.Transaction.retrieve(object_id=id)
#     print(transaction)
#     label_url = transaction.label_url

#     # Download the PDF file
#     response = requests.get(label_url)
#     print("\n", response)
#     if response.status_code == 200:
#         with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#             temp_file.write(response.content)
#             temp_file_path = temp_file.name
#         # Print the PDF file
#         printer_name = "HP_OfficeJet_Pro_8030_series"  # Replace with your printer name
#         print_command = f'lp -d {printer_name} {temp_file_path}'  # Use the appropriate print command for your operating system
#         # os.system(print_command)
#         try:
#             output = subprocess.check_output(print_command, stderr=subprocess.STDOUT, shell=True)
#             print(output.decode())
#             return "Label printed successfully"
#         except subprocess.CalledProcessError as e:
#             print(e.output.decode())
#             return "Failed to print the label"

#     return "Failed to download the label"
#     # return redirect(url_for("dashboard.dashboard"))


