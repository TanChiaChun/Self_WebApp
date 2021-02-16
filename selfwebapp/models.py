from selfwebapp import db, login_manager
from flask_login import UserMixin
from hashlib import blake2b

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User({self.username})"

def init_db():
    db.create_all()
    user1 = User(username="user1", password=blake2b(bytes("password1", "utf-8"), digest_size=20).hexdigest())
    db.session.add(user1)
    db.session.commit()