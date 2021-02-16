from flask import render_template, url_for, request, redirect, flash
from selfwebapp import app
from selfwebapp.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/proddash")
@login_required
def proddash():
    return render_template("proddash.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("inputUsername")
        password = request.form.get("inputPassword")
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash("Login successful", category="success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful", category="danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))