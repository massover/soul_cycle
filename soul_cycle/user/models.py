from datetime import datetime
from extensions import db, bcrypt

from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
        print self.password

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        return '<User %s>' % self.email
