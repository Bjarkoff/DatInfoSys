# save this as app.py
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "abcdEFGHw"
app.permanent_session_lifetime = timedelta(seconds= 30)

@app.route("/")
def home():
  if "user" in session:
    print("user in session")
    return render_template("index_logged_in.html")
  print("user not in session")
  return render_template("index_not_logged_in.html")  
  

@app.route("/login", methods = ["GET","POST"])
def login():
  if request.method == "POST":
    session.permanent = True
    user = request.form["username"]
    session["user"] = user
    flash("Succesful login!", "info")
    return redirect("/")
  else:
    if "user" in session:
      flash("Already logged in!", "info")
      return redirect("/")
    return render_template("login.html")
    
@app.route("/logout")
def logout():
  if "user" in session:
    user = session["user"]
    flash(f"user \'{user}\' has succesfully logged out!", "info")
  else:
    flash("No user to logout, please login below!")
  session.pop("user", None)  
  return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True) 