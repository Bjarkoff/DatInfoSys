# save this as app.py
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from queries import *
import re

app = Flask(__name__)
app.secret_key = "abcdEFGHw"
app.permanent_session_lifetime = timedelta(minutes= 5)

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

Event_pattern = re.compile("\[Event \"(.*?)\"\]", re.MULTILINE)
Date_pattern = re.compile("\[Date \"(.*?)\"\]", re.MULTILINE)
Round_pattern = re.compile("\[Round \"(.*?)\"\]", re.MULTILINE)
White_pattern = re.compile("\[White \"(.*?)\"\]", re.MULTILINE)
Black_pattern = re.compile("\[Black \"(.*?)\"\]", re.MULTILINE)
WhiteElo_pattern = re.compile("\[WhiteElo \"(.*?)\"\]", re.MULTILINE)
BlackElo_pattern = re.compile("\[BlackElo \"(.*?)\"\]", re.MULTILINE)
WhiteTeam_pattern = re.compile("\[WhiteTeam \"(.*?)\"\]", re.MULTILINE)
BlackTeam_pattern = re.compile("\[BlackTeam \"(.*?)\"\]", re.MULTILINE)
Result_pattern = re.compile("\[Result \"(.*?)\"\]", re.MULTILINE)
Board_pattern = re.compile("\[Board \"(.*?)\"\]", re.MULTILINE)
move_pattern = re.compile("\] ([10][a-zA-Z0-9 \.+\n\/-]*)", re.MULTILINE)
WhiteFideId_pattern = re.compile("\[WhiteFideId \"(.*?)\"\]", re.MULTILINE)
BlackFideId_pattern = re.compile("\[BlackFideId \"(.*?)\"\]", re.MULTILINE)

can_upload_query = '''
SELECT NOT EXISTS (SELECT 1
FROM chessgame
WHERE white_player = %s AND black_player = %s AND event = %s AND round = %s)
    '''


find_fideid_query = '''
SELECT fideid
FROM users 
WHERE username = %s
'''



@app.route("/upload", methods = ["GET","POST"])
def upload():
  conn = get_db_connection()
  cur = conn.cursor()
  username = session["user"]
  if request.method == "POST":
    pgn = request.form['PGN']
  
    if ((White_pattern.search(pgn)) == None or 
      (Black_pattern.search(pgn)) == None or
      (Date_pattern.search(pgn)) == None or
      (Result_pattern.search(pgn)) == None or
      (Board_pattern.search(pgn)) == None or
      (Round_pattern.search(pgn)) == None or
      (Event_pattern.search(pgn)) == None or
      (move_pattern.search(pgn)) == None or
      (WhiteFideId_pattern.search(pgn)) == None or
      (BlackFideId_pattern.search(pgn)) == None):
        cur.close()
        conn.close()
        return render_template("upload_results.html", pgn=pgn, upload = False)
    white = (WhiteFideId_pattern.search(pgn)).group(1)
    black = (BlackFideId_pattern.search(pgn)).group(1)
    cur.execute(find_fideid_query, (username,))
    fideID = cur.fetchone()[0]
    cur.execute(can_upload_query, (
      (WhiteFideId_pattern.search(pgn)).group(1), 
      (BlackFideId_pattern.search(pgn)).group(1), 
      (Event_pattern.search(pgn)).group(1), 
      (Round_pattern.search(pgn)).group(1), 
      ))
    can_update = cur.fetchone()
    if (can_update == None):
      cur.close()
      conn.close()
      return render_template("upload_results.html", pgn=pgn, upload = False)
    if (fideID == white or fideID == black) and can_update[0]:
      pgn_upload(pgn)
      cur.close()
      conn.close()
      return render_template("upload_results.html", pgn=pgn, upload = True)
    else:
      cur.close()
      conn.close()
      return render_template("upload_results.html", pgn=pgn, upload = False)
  else:
    cur.close()
    conn.close()
    return render_template("upload.html")





if __name__ == "__main__":
    app.run(debug=True) 
