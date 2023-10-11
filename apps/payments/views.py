import os
import uuid
import stripe
from flask_login import login_required
from apps.models import Image, Invoice, db
from apps import settings
from flask import Blueprint, request, render_template, redirect, url_for

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")
stripe.api_key = settings.STRIPE_SECRET_KEY

@payments_bp.route("/")
def render_form():
    return render_template('payments/pay.html')

@payments_bp.route("/list", methods=["GET"])
@login_required
def invoice_list():
    return render_template('payments/list.html')

@payments_bp.route("/form", methods=["GET"])
@login_required
def invoice_form():
    return render_template('payments/invoice_form.html')

@payments_bp.route("/create_invoice", methods=["POST"])
@login_required
def create_invoice():
    name = request.form['name']
    price = float(request.form['price'])
    images = []

    if 'images' in request.files:
        images_uploaded = request.files.getlist('images')  # Get all uploaded images as a list
        for image in images_uploaded:
            if image.filename != '':
                unique_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
                # Save the uploaded image with the unique filename
                image.save(os.path.join('static/img/', unique_filename))
                # Create a new Image record
                image_record = Image(invoice_id=None, url=unique_filename)
                # Append the image record to the 'images' list
                images.append(image_record)

    invoice = Invoice(name=name, price=price, images=images)

    # update DB
    db.session.add(invoice)
    for image in images:
        db.session.add(image)
    db.session.commit()
    
    return redirect(url_for("payments.invoice_list"))

@payments_bp.route("/pay", methods=["POST", "GET"])
def handle_payment():
    
    checkout_session = stripe.checkout.Session.create(
    payment_method_types=['card', 'affirm', 'afterpay_clearpay'],
    line_items=[{
        'price_data': {
        'currency': 'usd',
        'product_data': {
            'name': 'T-shirt',
        },
        'unit_amount': 5000,
        },
        'quantity': 1,
    }],
    mode='payment',
        shipping_address_collection={
    # Shipping address is optional but recommended to pass in
    # Specify which shipping countries Checkout should provide as options for shipping locations
    'allowed_countries': ['US'],
    },
   
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
    )
    return redirect(checkout_session.url, code=303)
