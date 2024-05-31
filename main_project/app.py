# save this as app.py
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from models import Player
import psycopg2

app = Flask(__name__)
app.secret_key = "abcdEFGHw"
app.permanent_session_lifetime = timedelta(seconds= 30)

def get_db_connection(): 
  conn = psycopg2.connect(host="localhost", dbname="DIS_project", user="bjarkerasmusnicolaisen", 
                        port="5432")
  return conn
conn = get_db_connection()
cur = conn.cursor()

# ------------------- Initializing a simple database with a few players: --------------------
cur.execute("DROP TABLE IF EXISTS players;")
cur.execute("DROP TABLE IF EXISTS chessgames;")
cur.execute("CREATE TABLE IF NOT EXISTS players (id INT," + 
            " username CHAR(100), password CHAR(100),rating REAL);")
test_player = Player("Bjarke",'righty',1780)
cur.execute("INSERT INTO players (id,username,password,rating) VALUES (%s,%s,%s,%s);", (
          test_player.id,
          test_player.username,
          test_player.password,
          test_player.rating,
      ))
cur.execute("CREATE TABLE IF NOT EXISTS chessgames (date DATE," + 
            " result CHAR(100), gameid INT,moves VARCHAR," +
            " round CHAR(100), event CHAR(100), board CHAR(100));")
cur.execute("INSERT INTO chessgames (date,result,gameid,board,round,event,moves) VALUES (%s,%s,%s,%s,%s,%s,%s);", (
          "2024-05-13",
          "1-0",
          "17",
          "7",
          "3.5",
          "Bundeslige 23-24",
          "1. e4 e5",
      ))
conn.commit()
cur.close()
conn.close()


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
    
    
    user = request.form["username"]
    password = request.form["password"]
    print(f"The username and password passed in: {user}, {password}")
    conn = get_db_connection()
    cur = conn.cursor()
    # Now we test if the entered user and password is in our database
    cur.execute(f"SELECT * FROM players p WHERE p.username = \'{user}\' AND p.password = \'{password}\';")
    user_list = cur.fetchall()
    print(f"The fetched list of existing users from database: {user_list}")
    if user_list == []:
      flash(f"User or password incorrect! Try again.")
      cur.close()
      conn.close()
      return redirect("/login")
    else:
      session.permanent = True 
      session["user"] = user
      flash(f"Succesful login! Welcome, {user}", "info")
      cur.close()
      conn.close()
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

@app.route("/register", methods = ["GET","POST"])
def register():
  if request.method == "POST":
    print("Are we here?")
    user     = request.form["username"]
    password = request.form["password"]
    rating   = request.form["rating"]
    conn = get_db_connection()
    cur = conn.cursor()
    # Now we test if the username is already in use in our database
    cur.execute(f"SELECT * FROM players p WHERE p.username = \'{user}\';")
    user_list = cur.fetchall()
    if user_list == []:
      new_player = Player(user,password,rating)
      cur.execute("INSERT INTO players (id,username,password,rating) VALUES (%s,%s,%s,%s);", (
          new_player.id,
          new_player.username,
          new_player.password,
          new_player.rating,
      ))
      conn.commit()
      flash(f"New user {user} registered succesfully!", "info")
      cur.close()
      conn.close()
      
      return redirect("/")
    else:
      flash(f"Username {user} already in use! Please choose another username.", "info")
      return redirect("/register")
  else:
    return render_template("register.html")

@app.route("/search", methods = ["GET", "POST"])
def search():
  if request.method == "POST":
    print("are we in the post-search branch?")
    conn = get_db_connection()
    cur = conn.cursor()
    query_results = []
    query_string = ""
    query_type  = request.form["type"]
    query_name  = request.form["name"]
    query_date  = request.form["date"]
    query_id    = request.form["gameid"]
    query_round = request.form["round"]
    query_event = request.form["event"]
    if query_type == "None":
      query_string = query_string + "SELECT * FROM chessgames"
      if query_date  != "":
        query_string = query_string + f" WHERE date = {query_date}"
      if query_id    != "":
        query_string = query_string + f" AND gameid = {query_id}"
      if query_round != "":
        query_string = query_string + f" AND round = {query_round}"
      if query_event != "":
        query_string = query_string + f" AND event = {query_event}"
      query_string = query_string + ";"
      cur.execute(query_string)
      query_results = cur.fetchall()
      conn.commit()
      cur.close()
      conn.close()
    elif query_type == "Team":
      pass
    else:
      pass
    return render_template("search_results_not_logged_in.html", entries = query_results)
  else:
    return render_template("search_database_not_logged_in.html")












if __name__ == "__main__":
    app.run(debug=True) 