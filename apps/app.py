from flask import Flask
from flask_migrate import Migrate
# shippo API app
from .label.views.form import label_bp
from .label.views.orders import dashboard_bp
from .models import db


# import settings
app = Flask(__name__)
app.config.from_pyfile('settings.py')
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# register blueprints
app.register_blueprint(label_bp)
app.register_blueprint(dashboard_bp)


# initialize database
migrate = Migrate(app, db)
db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()

