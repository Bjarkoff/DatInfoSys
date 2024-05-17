# save this as app.py
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "abcdEFGHw"
app.permanent_session_lifetime = timedelta(minutes= 5)


@app.route("/<name>")
def home(name):
    return render_template("index.html", content = f"{name}")

@app.route("/")
def home2():
    return render_template("index.html", content = "")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Succesful login!", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!", "info")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user = user)
    else:
        flash("You are not logged in! Please login below:","info")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"user \'{user}\' has succesfully logged out!", "info")
    else:
        flash("No user to logout, please login below!")
    session.pop("user", None)
    
    return redirect(url_for("login"))
""" @app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin/")
def admin():
    return redirect(url_for("user", name="Admin!")) """

if __name__ == "__main__":
    app.run(debug=True) 