from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from hashlib import blake2b
from datetime import date, datetime, timedelta
from selfwebapp import app, db
from selfwebapp.models import User, Key, Loop, Social, Day, Week, Month, Status

def get_curr_dt():
    return datetime.utcnow() + timedelta(hours=8)

def get_status_colour(frequency):
    rag_limits = {
        "Day": (1, 2),
        "Week": (7, 14),
        "Month": (28, 56)
    }
    d = Status.query.filter_by(frequency=frequency).first().last_done.date()
    d_defer = Status.query.filter_by(frequency=frequency).first().defer_to.date()
    diff = (get_curr_dt().date() - d).days
    if d_defer >= get_curr_dt().date():
        return ("#999999", "black")
    elif (diff < rag_limits[frequency][0]):
        return ("#7BB87B", "black")
    elif (diff < rag_limits[frequency][1]):
        return ("#FFCC33", "black")
    else:
        return ("#D2222D", "white")
app.jinja_env.globals["get_status_colour"] = get_status_colour

def get_item_colour(frequency, dt):
    rag_limits = {
        "Social": (0, 1, 2),
        "Day": (0, 1, 2),
        "Week": (1, 7, 14),
        "Month": (1, 28, 56)
    }
    if (frequency == "Key" or frequency == "Loop"):
        if dt.date() < get_curr_dt().date():
            return ("#D2222D", "white")
        hour_diff = (get_curr_dt() - dt).total_seconds() / 3600
        if hour_diff < 1:
            return ("#BDDBBD", "black")
        elif hour_diff < 2:
            return ("#7BB87B", "black")
        else:
            return ("#FFCC33", "black")
    else:
        diff = (get_curr_dt().date() - dt.date()).days
        if (diff < rag_limits[frequency][0]):
            return ("#BDDBBD", "black")
        elif (diff < rag_limits[frequency][1]):
            return ("#7BB87B", "black")
        elif (diff < rag_limits[frequency][2]):
            return ("#FFCC33", "black")
        else:
            return ("#D2222D", "white")
app.jinja_env.globals["get_item_colour"] = get_item_colour

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
    return render_template("status.html", statuses=statuses, curr_dt=get_curr_dt())

@app.route("/status/update/<int:s_id>")
@login_required
def status_update(s_id):
    status = Status.query.get_or_404(s_id)
    status.last_done_previous = status.last_done
    status.last_done = get_curr_dt()
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

@app.route("/productivity/<p>", methods=["GET", "POST"])
@login_required
def productivity(p):
    if request.method == "POST":
        if p == "week":
            productivity = Week.query.get_or_404(request.form["form_id"])
        elif p == "month":
            productivity = Month.query.get_or_404(request.form["form_id"])
        else:
            abort(404)
        productivity.last_check_previous = productivity.last_check
        productivity.last_check = datetime.strptime(request.form["manual_date"], "%Y-%m-%d")
        db.session.commit()
        flash(f"Manual updated {productivity.item} to {productivity.last_check.strftime('%#d %b %y')}", category="success")
        return redirect(url_for("productivity", p=p))
    if p == "key":
        productivities = Key.query.all()
    elif p == "loop":
        productivities = Loop.query.all()
    elif p == "social":
        productivities = Social.query.all()
    elif p == "day":
        productivities = Day.query.all()
    elif p == "week":
        productivities = Week.query.all()
    elif p == "month":
        productivities = Month.query.all()
    else:
        abort(404)
    return render_template(f"{p}.html", productivities=productivities, curr_dt=get_curr_dt(), p=p)

@app.route("/productivity/<p>/update/<int:p_id>")
@login_required
def productivity_update(p, p_id):
    if p == "key":
        productivity = Key.query.get_or_404(p_id)
    elif p == "loop":
        productivity = Loop.query.get_or_404(p_id)
    elif p == "social":
        productivity = Social.query.get_or_404(p_id)
    elif p == "day":
        productivity = Day.query.get_or_404(p_id)
    elif p == "week":
        productivity = Week.query.get_or_404(p_id)
    elif p == "month":
        productivity = Month.query.get_or_404(p_id)
    else:
        abort(404)
    productivity.last_check_previous = productivity.last_check
    productivity.last_check = get_curr_dt()
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
    elif p == "social":
        productivity = Social.query.get_or_404(p_id)
    elif p == "day":
        productivity = Day.query.get_or_404(p_id)
    elif p == "week":
        productivity = Week.query.get_or_404(p_id)
    elif p == "month":
        productivity = Month.query.get_or_404(p_id)
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
