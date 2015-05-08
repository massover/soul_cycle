from datetime import datetime
from extensions import db

from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<User %s>' % self.email
