from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required

transactions_bp = Blueprint("transactions", __name__, url_prefix="/dashboard")

@transactions_bp.route("/transactions", methods=["GET",])
@login_required
def transactions():
    return render_template("dashboard/order/order.html")
