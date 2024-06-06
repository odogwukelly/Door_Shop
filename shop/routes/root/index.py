from shop import app, db
from flask import render_template



@app.route("/", methods=["POST", "GET"])
def landing_page():
    return render_template("root/index.html")
