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

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String(80), unique=True, nullable=False)
    last_done = db.Column(db.DateTime, nullable=False)

class Productivity(object):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), unique=True, nullable=False)
    last_check = db.Column(db.DateTime, nullable=False)
    last_check_previous = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(80), nullable=False)

class Key(Productivity, db.Model):
    pass

class Loop(Productivity, db.Model):
    pass

def get_dt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")

def init_db(my_username, my_password, csv_paths):
    db.create_all()

    # Init user
    db.session.add(User(username=my_username, password=blake2b(bytes(my_password, "utf-8"), digest_size=20).hexdigest()))

    for csv_path in csv_paths:
        # Read from CSV
        items = []
        with open(csv_path) as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                items.append(row)
        
        # Init DB
        for i in items:
            if "Key" in csv_path:
                db.session.add(Key(item=i[1], last_check=get_dt(i[2]), last_check_previous=get_dt(i[3]), category=i[4]))
            elif "Loop" in csv_path:
                db.session.add(Loop(item=i[1], last_check=get_dt(i[2]), last_check_previous=get_dt(i[3]), category=i[4]))
            elif "Status" in csv_path:
                db.session.add(Status(frequency=i[1], last_done=get_dt(i[2])))
    
    db.session.commit()
