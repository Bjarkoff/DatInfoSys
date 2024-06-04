import psycopg2
from models import Player

def get_db_connection(): 
  conn = psycopg2.connect(host="localhost", dbname="teamchess", user="bjarkerasmusnicolaisen", 
                        port="5432", password="admin")
  return conn

def insert_new_user(username, password, fideid):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("INSERT INTO users (username,password,fideid) VALUES (%s,%s,%s);", (
      username,
      password,
      fideid,
  ))
  conn.commit()
  cur.close()
  conn.close()

def test_register(username,fideID):
  return test_username_in_users(username) == False and test_fideID_in_players(fideID) and not test_fideID_in_users(fideID)

def test_username_in_users(name):
  conn = get_db_connection()
  cur = conn.cursor()
  # Now we test if the entered user and password is in our database
  cur.execute(f"SELECT * FROM users p WHERE p.username = \'{name}\';")
  user_list = cur.fetchall()
  cur.close()
  conn.close()
  return user_list != []

def test_fideID_in_players(fideID):
  conn = get_db_connection()
  cur = conn.cursor()
  # Now we test if the entered fideID is in our database from players
  cur.execute(f"SELECT * FROM players p WHERE p.fideid = \'{fideID}\';")
  user_list = cur.fetchall()
  cur.close()
  conn.close()
  return user_list != []                                  

def test_fideID_in_users(fideID):
  conn = get_db_connection()
  cur = conn.cursor()
  # Now we test if the entered fideID is in our database from users
  cur.execute(f"SELECT * FROM users p WHERE p.fideid = \'{fideID}\';")
  user_list = cur.fetchall()
  cur.close()
  conn.close()
  return user_list != [] 

def test_username_and_password(name,password):
  conn = get_db_connection()
  cur = conn.cursor()
  # Now we test if the entered user and password is in our database
  cur.execute(f"SELECT * FROM users p WHERE p.username = \'{name}\' AND p.password = \'{password}\';")
  user_list = cur.fetchall()
  cur.close()
  conn.close()
  return user_list != []

def get_chessgames_by_filters(date=None, event=None, player_name=None, team_name=None,
                           game_id=None, round=None):
  sql = """
  SELECT p1.name, t1.team_name, p2.name, t2.team_name, date, result, round, event, moves FROM chessgame g, players p1, players p2, playerteams t1, playerteams t2 WHERE
	g.white_player = p1.fideid AND
	g.black_player = p2.fideid AND 
	p1.fideid = t1.fideid AND
	p2.fideid = t2.fideid
  """
  if player_name != '':
    sql = sql + f" AND (p1.name='{player_name}' OR p2.name='{player_name}')"
  if team_name != '':
    sql = sql + f" AND (t1.team_name='{team_name}' OR t2.team_name='{team_name}')" 
  if date != '':
    sql = sql + f" AND date='{date}'"
  if event != '':
    sql = sql + f" AND event = '{event}'"
  if game_id != '':
    sql = sql + f" AND game_id = '{game_id}'"
  if round != '':
    sql = sql + f" AND round = '{round}'"
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(sql)
  chessgames = cur.fetchall()
  cur.close()
  conn.close()
  return chessgames

def get_players_teamname(name):
  sql = f"SELECT team_name FROM users p, playerteams pt WHERE p.fideid = pt.fideid AND p.username = '{name}'"
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(sql)
  teamname = cur.fetchall()
  cur.close()
  conn.close()
  return teamname