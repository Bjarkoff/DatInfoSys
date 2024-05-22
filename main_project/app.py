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
cur.execute("CREATE TABLE IF NOT EXISTS players (id INT," + 
            " username CHAR(100), password CHAR(100),rating REAL);")
test_player = Player("Bjarke",'righty',1780)
cur.execute("INSERT INTO players (id,username,password,rating) VALUES (%s,%s,%s,%s);", (
          test_player.id,
          test_player.username,
          test_player.password,
          test_player.rating,
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



if __name__ == "__main__":
    app.run(debug=True) 