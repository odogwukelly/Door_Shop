from shop import app

@app.route("/")
def home_page():
    return "hello world"