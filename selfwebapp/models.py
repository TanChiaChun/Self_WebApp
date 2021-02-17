from selfwebapp import db, login_manager
from flask_login import UserMixin
from hashlib import blake2b
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User({self.username})"

class Productivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), unique=True, nullable=False)
    last_check = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Productivity({self.item}: {self.last_check})"

def init_db():
    db.create_all()
    # user1 = User(username="user1", password=blake2b(bytes("password1", "utf-8"), digest_size=20).hexdigest())
    # db.session.add(user1)
    prod1 = Productivity(item="Calendar", last_check=datetime.utcnow())
    prod2 = Productivity(item="To Do", last_check=datetime.utcnow())
    prod3 = Productivity(item="CNET Tech Today", last_check=datetime.utcnow())
    prod4 = Productivity(item="Email", last_check=datetime.utcnow())
    prod5 = Productivity(item="WhatsApp", last_check=datetime.utcnow())
    prod6 = Productivity(item="Telegram", last_check=datetime.utcnow())
    prod7 = Productivity(item="Messenger", last_check=datetime.utcnow())
    prod8 = Productivity(item="Photo", last_check=datetime.utcnow())
    db.session.add(prod1)
    db.session.add(prod2)
    db.session.add(prod3)
    db.session.add(prod4)
    db.session.add(prod5)
    db.session.add(prod6)
    db.session.add(prod7)
    db.session.add(prod8)
    db.session.commit()