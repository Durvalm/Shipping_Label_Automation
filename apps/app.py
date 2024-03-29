from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
# shippo API app
from apps.label.views.form import label_bp
from apps.label.views.orders import dashboard_bp
from apps.label.views.transactions import transactions_bp
from apps.payments.views import payments_bp

from apps.auth.views import auth_bp
from apps.models import db, SuperUser

import os


# import settings
app = Flask(__name__)
app.config.from_pyfile('settings.py')

# register blueprints
app.register_blueprint(label_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(payments_bp)

# initialize database
migrate = Migrate(app, db)
db.init_app(app)
with app.app_context():
    db.create_all()

# login
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    # Load user from the database based on the provided user_id
    return SuperUser.query.get(int(user_id))

login_manager.init_app(app)
login_manager.login_view = 'auth.login'


if __name__ == '__main__':
    app.run()

