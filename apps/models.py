from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    country = db.Column(db.String(64), unique=False, nullable=False)
    street1 = db.Column(db.String(255), unique=False, nullable=False)
    street2 = db.Column(db.String(255), unique=False, nullable=True)
    city = db.Column(db.String(64), unique=False, nullable=False)
    state = db.Column(db.String(64), unique=False, nullable=False)
    zipcode = db.Column(db.String(20), unique=False, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=True)
    rate = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return f'{self.name}'

