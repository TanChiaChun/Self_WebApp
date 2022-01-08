from flask_login import UserMixin
from hashlib import blake2b
from datetime import datetime
from selfwebapp import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Productivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), unique=True, nullable=False)
    last_check = db.Column(db.DateTime, nullable=False)
    last_check_previous = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(80), nullable=False)

def init_db(my_username, my_password):
    db.create_all()
    user1 = User(username=my_username, password=blake2b(bytes(my_password, "utf-8"), digest_size=20).hexdigest())
    db.session.add(user1)
    db.session.commit()
