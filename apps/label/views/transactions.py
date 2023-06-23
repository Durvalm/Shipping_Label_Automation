from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required
from apps.models import db, User
import shippo
from apps.settings import PARCEL, ADDRESS_FROM, SHIPPO_API_TOKEN
from .orders import create_shipping, create_shipping_service
 
shippo.config.api_key = SHIPPO_API_TOKEN

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")

@transactions_bp.route("", methods=["GET",])
@login_required
def transactions():
    # If name is searched, display users with name
    if request.args.get('name'):
        users = User.query.filter(User.name.ilike(f"%{request.args.get('name')}%")).all()
    # All users
    else:
        users = User.query.filter_by().order_by(User.created_at.desc()).all()
    return render_template("dashboard/order/order.html", users=users)

@transactions_bp.route("/create-new-label", methods=["POST",])
@login_required
def create_new_label():
    # Update Address
    address_data = {key: request.form[key] for key in ['name', 'country', 'street1', 'street2', 'state', 'city', 'zipcode']}
    user = User(**address_data)
    db.session.add(user)
    db.session.commit()
    
    shipment = create_shipping(user)
    create_shipping_service(user, shipment)
 
    return redirect(url_for('dashboard.confirm_purchase', user_id=user.id))


@transactions_bp.route("/search", methods=["POST",])
@login_required
def search_order():
    name = request.form["name"]
    query_params = {'name': name}
    return redirect(url_for('transactions.transactions', **query_params))
  

@transactions_bp.route("/remove/<int:user_id>", methods=["POST", "DELETE", "GET"])
@login_required
def remove_order(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('transactions.transactions'))

