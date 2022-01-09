from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from hashlib import blake2b
from datetime import date, datetime, timedelta
from selfwebapp import app, db
from selfwebapp.models import User, Key, Loop, Status

def get_status_diff(frequency):
    rag_limits = {
        "Day": (1, 2),
        "Week": (7, 14),
        "Month": (28, 56)
    }
    d = Status.query.filter_by(frequency=frequency).first().last_done.date()
    diff = (date.today() - d).days
    if (diff < rag_limits[frequency][0]):
        return ("#7BB87B", "black")
    elif (diff < rag_limits[frequency][1]):
        return ("#FFCC33", "black")
    else:
        return ("#D2222D", "white")
app.jinja_env.globals["get_status_diff"] = get_status_diff

@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/status", methods=["GET", "POST"])
@login_required
def status():
    if request.method == "POST":
        status = Status.query.get_or_404(request.form["form_id"])
        status.defer_to = datetime.strptime(request.form["defer_date"], "%Y-%m-%d")
        db.session.commit()
        flash(f"Deferred {status.frequency} to {status.defer_to.strftime('%#d %b %y')}", category="success")
        return redirect(url_for("status"))
    statuses = Status.query.all()
    return render_template("status.html", statuses=statuses)

@app.route("/status/update/<int:s_id>")
@login_required
def status_update(s_id):
    status = Status.query.get_or_404(s_id)
    status.last_done_previous = status.last_done
    status.last_done = datetime.utcnow() + timedelta(hours=8)
    db.session.commit()
    flash(f"Updated {status.frequency}", category="success")
    return redirect(url_for("status"))

@app.route("/status/undo/<int:s_id>")
@login_required
def status_undo(s_id):
    status = Status.query.get_or_404(s_id)
    status.last_done = status.last_done_previous
    db.session.commit()
    flash(f"Undo {status.frequency}", category="success")
    return redirect(url_for("status"))

@app.route("/productivity/<p>")
@login_required
def productivity(p):
    curr_datetime = datetime.utcnow() + timedelta(hours=8)
    if p == "key":
        productivities = Key.query.all()
    elif p == "loop":
        productivities = Loop.query.all()
    else:
        abort(404)
    return render_template(f"{p}.html", productivities=productivities, curr_datetime=curr_datetime, p=p)

@app.route("/productivity/<p>/update/<int:p_id>")
@login_required
def productivity_update(p, p_id):
    if p == "key":
        productivity = Key.query.get_or_404(p_id)
    elif p == "loop":
        productivity = Loop.query.get_or_404(p_id)
    else:
        abort(404)
    productivity.last_check_previous = productivity.last_check
    productivity.last_check = datetime.utcnow() + timedelta(hours=8)
    db.session.commit()
    flash(f"Updated {productivity.item}", category="success")
    return redirect(url_for("productivity", p=p))

@app.route("/productivity/<p>/undo/<int:p_id>")
@login_required
def productivity_undo(p, p_id):
    if p == "key":
        productivity = Key.query.get_or_404(p_id)
    elif p == "loop":
        productivity = Loop.query.get_or_404(p_id)
    else:
        abort(404)
    productivity.last_check = productivity.last_check_previous
    db.session.commit()
    flash(f"Undo {productivity.item}", category="success")
    return redirect(url_for("productivity", p=p))

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
