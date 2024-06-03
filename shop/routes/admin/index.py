from shop import app

@app.route("/admin", methods=["GET", "POST"])
def dashboard():
    return "greeting"