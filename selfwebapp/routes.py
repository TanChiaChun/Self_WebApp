from flask import render_template, url_for
from selfwebapp import app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/proddash")
def proddash():
    return render_template("proddash.html")