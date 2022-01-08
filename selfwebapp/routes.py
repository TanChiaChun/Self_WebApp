from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from hashlib import blake2b
from datetime import datetime, timedelta
from selfwebapp import app, db
from selfwebapp.models import User, Productivity

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/hour")
@login_required
def hour():
    prods = Productivity.query.all()
    curr_datetime = datetime.utcnow() + timedelta(hours=8)
    return render_template("hour.html", prods=prods, curr_datetime=curr_datetime)

@app.route("/hour/update/<int:prod_id>")
@login_required
def hour_update(prod_id):
    prod = Productivity.query.get_or_404(prod_id)
    prod.last_check_previous = prod.last_check
    prod.last_check = datetime.utcnow() + timedelta(hours=8)
    db.session.commit()
    flash(f"Updated {prod.item}", category="success")
    return redirect(url_for("hour"))

@app.route("/hour/undo/<int:prod_id>")
@login_required
def hour_undo(prod_id):
    prod = Productivity.query.get_or_404(prod_id)
    prod.last_check = prod.last_check_previous
    db.session.commit()
    flash(f"Undo {prod.item}", category="success")
    return redirect(url_for("hour"))

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
