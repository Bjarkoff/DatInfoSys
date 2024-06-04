# save this as app.py
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from models import Player
import psycopg2
from queries import *

app = Flask(__name__)
app.secret_key = "abcdEFGHw"
app.permanent_session_lifetime = timedelta(minutes= 5)

conn = get_db_connection()
cur = conn.cursor()

# ------------------------------------- Routing and core functionality ----------------------------------

@app.route("/")
def home():
  if "user" in session:
    return render_template("index_logged_in.html")
  return render_template("index_not_logged_in.html")  
  

@app.route("/login", methods = ["GET","POST"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    if test_username_and_password(username,password) == False:
      flash(f"User or password incorrect! Try again.", "info")
      return redirect("/login")
    else:
      session.permanent = True 
      session["user"] = username
      flash(f"Succesful login! Welcome, {username}", "info")
    return redirect("/")
  else:
    if "user" in session:
      flash("Already logged in!", "info")
      return redirect("/")
    return render_template("login.html")
    
@app.route("/logout")
def logout():
  if "user" in session:
    username = session["user"]
    flash(f"user \'{username}\' has succesfully logged out!", "info")
  else:
    flash("No user to logout, please login below!")
  session.pop("user", None)  
  return redirect(url_for("login"))

@app.route("/register", methods = ["GET","POST"])
def register():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    fideID   = request.form["fideID"]
    if test_register(username,fideID):
      flash(f"New user {username} registered succesfully!", "info")
      insert_new_user(username, password, fideID)
      return redirect("/")
    else:
      flash(f"Username {username} or fideID {fideID} already in use, or fideID does not exist!", "info")
      return redirect("/register")
  else:
    return render_template("register.html")

@app.route("/search", methods = ["GET", "POST"])
def search():
  if request.method == "POST":
    query_teamname    = request.form["team_name"]
    query_playername  = request.form["player_name"]
    query_date        = request.form["date"]
    query_id          = request.form["gameid"]
    query_round       = request.form["round"]
    query_event       = request.form["event"]
    query_results = get_chessgames_by_filters(query_date,query_event,query_playername,
                                              query_teamname,query_id,query_round)

    if "user" in session:
      team_name = get_players_teamname(session["user"])
      return render_template("search_results_logged_in.html", entries = query_results, team_name = team_name[0][0])
    else:
      return render_template("search_results_not_logged_in.html", entries = query_results)
  else:
    if "user" in session:
      return render_template("search_database_logged_in.html")
    return render_template("search_database_not_logged_in.html")

@app.route("/upload", methods = ["GET","POST"])
def upload():
  if request.method == "POST":
    pgn = request.form['PGN']
    return render_template("upload_results.html", pgn=pgn)
  else:
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True) 
