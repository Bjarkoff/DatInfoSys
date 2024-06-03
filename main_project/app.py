# save this as app.py
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from models import Player
import psycopg2

app = Flask(__name__)
app.secret_key = "abcdEFGHw"
app.permanent_session_lifetime = timedelta(minutes= 5)

def get_db_connection(): 
  conn = psycopg2.connect(host="localhost", dbname="DIS_project", user="bjarkerasmusnicolaisen", 
                        port="5432", password="admin")
  return conn
conn = get_db_connection()
cur = conn.cursor()

# ------------------- Initializing a simple database with a few players: --------------------
cur.execute("DROP TABLE IF EXISTS players;")
cur.execute("DROP TABLE IF EXISTS chessgames;")
cur.execute("DROP TABLE IF EXISTS teams;")
cur.execute("DROP TABLE IF EXISTS plays;")
cur.execute("DROP TABLE IF EXISTS player_teams")
cur.execute("CREATE TABLE players (id INT," + 
            " username CHAR(100), password CHAR(100),rating REAL);")
test_player = Player("Bjarke",'righty',1780)
test_player2 = Player("Oscar",'test',1980)
test_player3 = Player("Niels","test",1000)
test_player4 = Player("Dragos","test",2500)
cur.execute("INSERT INTO players (id,username,password,rating) VALUES (%s,%s,%s,%s);", (
          test_player.id,
          test_player.username,
          test_player.password,
          test_player.rating,
      ))
cur.execute("INSERT INTO players (id,username,password,rating) VALUES (%s,%s,%s,%s);", (
          test_player2.id,
          test_player2.username,
          test_player2.password,
          test_player2.rating,
      ))
cur.execute("INSERT INTO players (id,username,password,rating) VALUES (%s,%s,%s,%s);", (
          test_player3.id,
          test_player3.username,
          test_player3.password,
          test_player3.rating,
      ))
cur.execute("INSERT INTO players (id,username,password,rating) VALUES (%s,%s,%s,%s);", (
          test_player4.id,
          test_player4.username,
          test_player4.password,
          test_player4.rating,
      ))
cur.execute("CREATE TABLE plays (player INT, color CHAR(10),game_id INT);")
cur.execute("INSERT INTO plays (player, color, game_id) VALUES (%s, %s, %s);", 
            (test_player.id, "Black", "17"))
cur.execute("INSERT INTO plays (player, color, game_id) VALUES (%s, %s, %s);", 
            (test_player2.id, "White", "17"))
cur.execute("INSERT INTO plays (player, color, game_id) VALUES (%s, %s, %s);", 
            (test_player3.id, "White", "16"))
cur.execute("INSERT INTO plays (player, color, game_id) VALUES (%s, %s, %s);", 
            (test_player4.id, "Black", "16"))
cur.execute("CREATE TABLE chessgames (date DATE," + 
            " result CHAR(100), gameid INT,moves VARCHAR," +
            " round CHAR(100), event CHAR(100), board CHAR(100));")
cur.execute("INSERT INTO chessgames (date,result,gameid,board,round,event,moves) VALUES (%s,%s,%s,%s,%s,%s,%s);", (
          "2024-05-13",
          "1-0",
          "17",
          "7",
          "3.5",
          "Bundesliga 23-24",
          "1. e4 e5",
      ))
cur.execute("INSERT INTO chessgames (date,result,gameid,board,round,event,moves) VALUES (%s,%s,%s,%s,%s,%s,%s);", (
          "2024-05-13",
          "1/2-1/2",
          "16",
          "6",
          "3.5",
          "Bundesliga 23-24",
          "1. e4 d5",
      ))
cur.execute("CREATE TABLE teams (name CHAR(100), event CHAR(100))")
cur.execute("INSERT INTO teams (name, event) VALUES (%s,%s);", ("team1","Bundesliga 23-24",))
cur.execute("INSERT INTO teams (name, event) VALUES (%s,%s);", ("team2","Bundesliga 23-24",))
cur.execute("CREATE TABLE player_teams (player_id INT, team_name CHAR(100))")
cur.execute("INSERT INTO player_teams (player_id, team_name) VALUES (%s,%s);", (test_player.id,"team1"))
cur.execute("INSERT INTO player_teams (player_id, team_name) VALUES (%s,%s);", (test_player2.id,"team2"))
cur.execute("INSERT INTO player_teams (player_id, team_name) VALUES (%s,%s);", (test_player3.id,"team1"))
cur.execute("INSERT INTO player_teams (player_id, team_name) VALUES (%s,%s);", (test_player4.id,"team2"))

conn.commit()
cur.close()
conn.close()




# ---------------------------- Logic for querying database later -------------------------------

def get_chessgames_by_filters(date=None, event=None, player_name=None, team_name=None,
                           game_id=None, round=None):
  sql = """
  SELECT pl1.username, plt1.team_name, pl2.username, plt2.team_name date, result, moves FROM players pl1, players pl2, plays p1, plays p2, chessgames g, player_teams plt1, player_teams plt2 WHERE
p1.player <> p2.player AND g.gameid = p1.game_id AND p2.game_id = p1.game_id
AND pl1.id = p1.player AND pl2.id = p2.player AND p1.color = 'White'
AND plt1.player_id = pl1.id AND plt2.player_id = pl2.id
  """
  conditionals = []
  print(player_name)
  print(player_name == True)
  if player_name != '':
    sql = sql + f" AND (pl1.username='{player_name}' OR pl2.username='{player_name}')"
  if team_name != '':
    sql = sql + f" AND (plt1.team_name='{team_name}' OR plt2.team_name='{team_name}')" 
  if date != '':
    sql = sql + f" AND date='{date}'"
  if event != '':
    sql = sql + f" AND event = '{event}'"
  if game_id != '':
    sql = sql + f" AND game_id = '{game_id}'"
  if round != '':
    sql = sql + f" AND round = '{round}'"
  print(sql)
  #args_str = ' AND '.join(conditionals)
  # order = " ORDER BY rating "
  #print(sql + args_str)
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(sql)
  # db_cursor.execute(sql + args_str + order)
  # chessgames = [Produce(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
  chessgames = cur.fetchall()
  # conn.commit()
  cur.close()
  conn.close()
  return chessgames

def get_players_teamname(name):
  sql = f"SELECT team_name FROM players p, player_teams pt WHERE p.id = pt.player_id AND p.username = '{name}'"
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(sql)
  teamname = cur.fetchall()
  cur.close()
  conn.close()
  return teamname
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
    conn = get_db_connection()
    cur = conn.cursor()
    query_results = []
    query_teamname    = request.form["team_name"]
    query_playername  = request.form["player_name"]
    query_date        = request.form["date"]
    query_id          = request.form["gameid"]
    query_round       = request.form["round"]
    query_event       = request.form["event"]
    query_results = get_chessgames_by_filters(query_date,query_event,query_playername,
                                              query_teamname,query_id,query_round)

    if "user" in session:
      username = get_players_teamname(session["user"])
      return render_template("search_results_logged_in.html", entries = query_results, team_name = username[0][0])
    else:
      return render_template("search_results_not_logged_in.html", entries = query_results)
  else:
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
