from shop import app
from flask import render_template

@app.route("/register", methods=["POST", "GET"])
def register():
    return render_template("/root/registration.html")