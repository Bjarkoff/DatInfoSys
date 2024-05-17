# save this as app.py
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    return render_template("index.html", content = f"{name}")

@app.route("/")
def home2():
    return render_template("index.html", content = "")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return render_template("index.html", content = f"{usr}")

""" @app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin/")
def admin():
    return redirect(url_for("user", name="Admin!")) """

if __name__ == "__main__":
    app.run(debug=True) 