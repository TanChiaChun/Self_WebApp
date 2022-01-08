from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from hashlib import blake2b
from datetime import datetime, timedelta
from selfwebapp import app, db
from selfwebapp.models import User, Key

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/key")
@login_required
def key():
    keys = Key.query.all()
    curr_datetime = datetime.utcnow() + timedelta(hours=8)
    return render_template("key.html", keys=keys, curr_datetime=curr_datetime)

@app.route("/key/update/<int:key_id>")
@login_required
def key_update(key_id):
    key = Key.query.get_or_404(key_id)
    key.last_check_previous = key.last_check
    key.last_check = datetime.utcnow() + timedelta(hours=8)
    db.session.commit()
    flash(f"Updated {key.item}", category="success")
    return redirect(url_for("key"))

@app.route("/key/undo/<int:key_id>")
@login_required
def key_undo(key_id):
    key = Key.query.get_or_404(key_id)
    key.last_check = key.last_check_previous
    db.session.commit()
    flash(f"Undo {key.item}", category="success")
    return redirect(url_for("key"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("inputUsername")
        password = bytes(request.form.get("inputPassword"), "utf-8")
        user = User.query.filter_by(username=username).first()
        if user and blake2b(password, digest_size=20).hexdigest() == user.password:
            login_user(user, remember=True, duration=timedelta(weeks=2))
            flash("Login successful", category="success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful", category="danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful", category="success")
    return redirect(url_for("login"))
