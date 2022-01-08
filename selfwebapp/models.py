from flask_login import UserMixin
from hashlib import blake2b
import csv
from datetime import datetime
from selfwebapp import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), unique=True, nullable=False)
    last_check = db.Column(db.DateTime, nullable=False)
    last_check_previous = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(80), nullable=False)

def get_dt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")

def init_db(my_username, my_password, csv_path):
    db.create_all()

    # Init user
    user1 = User(username=my_username, password=blake2b(bytes(my_password, "utf-8"), digest_size=20).hexdigest())
    db.session.add(user1)

    # Read Keys from CSV
    keys = []
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            keys.append(row)
    
    # Init Keys
    for p in keys:
        db.session.add(Key(item=p[1], last_check=get_dt(p[2]), last_check_previous=get_dt(p[3]), category=p[4]))
    
    db.session.commit()
