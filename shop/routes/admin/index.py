from shop import app
from flask import render_template

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("/admin/dashboard.html")