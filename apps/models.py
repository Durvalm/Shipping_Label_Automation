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
    is_my_address = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'{self.name}'

# class Shipping(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     user = db.relationship("User", backref=db.backref("shippings", lazy=True))

#     def __repr__(self):
#         return f'{self.user.name}'
