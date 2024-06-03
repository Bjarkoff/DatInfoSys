import psycopg2
from models import Player

def get_db_connection(): 
  conn = psycopg2.connect(host="localhost", dbname="DIS_project", user="bjarkerasmusnicolaisen", 
                        port="5432", password="admin")
  return conn

def insert_new_player(username, password, rating):
  conn = get_db_connection()
  cur = conn.cursor()
  new_player = Player(username,password,rating)
  cur.execute("INSERT INTO players (id,username,password,rating) VALUES (%s,%s,%s,%s);", (
      new_player.id,
      new_player.username,
      new_player.password,
      new_player.rating,
  ))
  conn.commit()
  cur.close()
  conn.close()



def test_username(name):
  conn = get_db_connection()
  cur = conn.cursor()
  # Now we test if the entered user and password is in our database
  cur.execute(f"SELECT * FROM players p WHERE p.username = \'{name}\';")
  user_list = cur.fetchall()
  cur.close()
  conn.close()
  return user_list != []

def test_username_and_password(name,password):
  conn = get_db_connection()
  cur = conn.cursor()
  # Now we test if the entered user and password is in our database
  cur.execute(f"SELECT * FROM players p WHERE p.username = \'{name}\' AND p.password = \'{password}\';")
  user_list = cur.fetchall()
  cur.close()
  conn.close()
  return user_list != []

def get_chessgames_by_filters(date=None, event=None, player_name=None, team_name=None,
                           game_id=None, round=None):
  sql = """
  SELECT pl1.username, plt1.team_name, pl2.username, plt2.team_name date, result, moves FROM players pl1, players pl2, plays p1, plays p2, chessgames g, player_teams plt1, player_teams plt2 WHERE
p1.player <> p2.player AND g.gameid = p1.game_id AND p2.game_id = p1.game_id
AND pl1.id = p1.player AND pl2.id = p2.player AND p1.color = 'White'
AND plt1.player_id = pl1.id AND plt2.player_id = pl2.id
  """
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
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(sql)
  chessgames = cur.fetchall()
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