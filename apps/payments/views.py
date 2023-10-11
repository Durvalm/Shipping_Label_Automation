import stripe
from apps import settings
from flask import Blueprint, request, render_template, redirect, url_for

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")
stripe.api_key = settings.STRIPE_SECRET_KEY

@payments_bp.route("/")
def render_form():
    return render_template('payments/pay.html')


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