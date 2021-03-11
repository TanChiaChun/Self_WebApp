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

    def __repr__(self):
        return f"User({self.username})"

class Productivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), unique=True, nullable=False)
    last_check = db.Column(db.DateTime, nullable=False)
    last_check_previous = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Productivity({self.item}: {self.last_check})"

def init_db(my_username, my_password):
    db.create_all()
    user1 = User(username=my_username, password=blake2b(bytes(my_password, "utf-8"), digest_size=20).hexdigest())
    db.session.add(user1)
    prod1 = Productivity(item="Calendar", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Key")
    prod2 = Productivity(item="To Do", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Key")
    prod3 = Productivity(item="WhatsApp", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Messaging")
    prod4 = Productivity(item="Telegram", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Messaging")
    prod5 = Productivity(item="Messenger", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Messaging")
    prod6 = Productivity(item="Teams", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Messaging")
    prod7 = Productivity(item="Telegram - Photos", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Photos")
    prod8 = Productivity(item="Photos", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Photos")
    prod9 = Productivity(item="Photos - Albums", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="Photos")
    prod10 = Productivity(item="CNET Tech Today", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="News")
    prod11 = Productivity(item="Emails", last_check=datetime.utcnow(), last_check_previous=datetime.utcnow(), category="News")
    db.session.add(prod1)
    db.session.add(prod2)
    db.session.add(prod3)
    db.session.add(prod4)
    db.session.add(prod5)
    db.session.add(prod6)
    db.session.add(prod7)
    db.session.add(prod8)
    db.session.add(prod9)
    db.session.add(prod10)
    db.session.add(prod11)
    db.session.commit()