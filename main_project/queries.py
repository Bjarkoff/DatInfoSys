import psycopg2
from models import Player
import re
from psycopg2 import sql

def get_db_connection(): 
  conn = psycopg2.connect(host="localhost", dbname="teamchess", user="postgres", 
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




def pgn_upload(pgn):
  conn = get_db_connection()
  cur = conn.cursor()
  tmp = pgn
  event = Event_pattern.findall(tmp)
  date = Date_pattern.findall(tmp)
  round = Round_pattern.findall(tmp)
  move = move_pattern.findall(tmp)
  white = White_pattern.findall(tmp)
  black = Black_pattern.findall(tmp)
  whitelo = WhiteElo_pattern.findall(tmp)
  BlackElo = BlackElo_pattern.findall(tmp)
  WhiteFideId = WhiteFideId_pattern.findall(tmp)
  BlackFideId = BlackFideId_pattern.findall(tmp)
  WhiteTeam = WhiteTeam_pattern.findall(tmp)
  BlackTeam = BlackTeam_pattern.findall(tmp)
  Result = Result_pattern.findall(tmp)
  move = move_pattern.findall(tmp)
  Board = Board_pattern.findall(tmp)


  for i in range(len(white)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Players WHERE name = %s)", (white[i],))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute(
            sql.SQL("INSERT INTO Players (name, elo, FideId) VALUES (%s, %s,%s)"),
            (white[i], whitelo[i],WhiteFideId[i])
        )
        conn.commit()

  for i in range(len(black)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM Players WHERE name = %s)", (black[i],))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute(
              sql.SQL("INSERT INTO Players (name, elo, FideId) VALUES (%s, %s, %s)"),
              (black[i], BlackElo[i], BlackFideId[i])
          )
          conn.commit()

  for i in range(len(WhiteTeam)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM Teams WHERE Team_name = %s)", (WhiteTeam[i],))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO Teams (Team_name) VALUES (%s)", (WhiteTeam[i],))
          conn.commit()

  for i in range(len(BlackTeam)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM Teams WHERE Team_name = %s)", (BlackTeam[i],))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO Teams (Team_name) VALUES (%s)", (WhiteTeam[i],))
          conn.commit()

  for i in range(len(WhiteFideId)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM PlayerTeams WHERE FideId = %s AND team_name = %s)", (WhiteFideId[i], WhiteTeam[i]))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO PlayerTeams (FideId, team_name) VALUES (%s, %s)", (WhiteFideId[i],WhiteTeam[i]))
          conn.commit()

  for i in range(len(BlackFideId)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM PlayerTeams WHERE FideId = %s AND team_name = %s)", (BlackFideId[i], BlackTeam[i]))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO PlayerTeams (FideId, team_name) VALUES (%s, %s)", (BlackFideId[i],BlackTeam[i]))
          conn.commit()

  for i in range(len(event)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM Leagues WHERE Event = %s )", (event[i], ))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO Leagues (Event) VALUES (%s)", (event[i],))
          conn.commit()


  for i in range(len(event)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM League_Teams WHERE Event = %s AND team_name = %s )", (event[i], WhiteTeam[i]))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO League_Teams (Event, team_name) VALUES (%s, %s)", (event[i],WhiteTeam[i]))
          conn.commit()

  for i in range(len(event)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM League_Teams WHERE Event = %s AND team_name = %s )", (event[i], BlackTeam[i]))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO League_Teams (Event, team_name) VALUES (%s, %s)", (event[i],BlackTeam[i]))
          conn.commit()


  for i in range(len(round)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM Team_match WHERE Event = %s AND round = %s )", (event[i], round[i]))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO Team_match (Event, round) VALUES (%s, %s)", (event[i],round[i]))
          conn.commit()



  for i in range(len(WhiteTeam)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM battle_in WHERE Team_name = %s AND round = %s AND Event = %s )", (WhiteTeam[i], round[i], event[i]))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO battle_in (Team_name, round, Event) VALUES (%s, %s, %s)", (WhiteTeam[i],round[i],event[i]))
          conn.commit()

  for i in range(len(BlackTeam)):
      cur.execute("SELECT EXISTS(SELECT 1 FROM battle_in WHERE Team_name = %s AND round = %s AND Event = %s )", (BlackTeam[i], round[i], event[i]))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO battle_in (Team_name, round, Event) VALUES (%s, %s, %s)", (BlackTeam[i],round[i],event[i]))
          conn.commit()


  cur.execute("SELECT MAX(CAST(game_id AS int))FROM chessgame")
  game_id = cur.fetchone()[0] + 1


  print(len(move))
  for i in range(len(move)):
      print("hej!!")
      cur.execute("SELECT EXISTS(SELECT 1 FROM Chessgame WHERE white_player = %s AND black_player = %s AND Event = %s AND round = %s)", (WhiteFideId[i], BlackFideId[i], event[i], round[i]))
      record_exists = cur.fetchone()[0]
      if not record_exists:
          cur.execute("INSERT INTO Chessgame (white_player, black_player, Date, game_id, moves, round, Event, board, result) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)", (WhiteFideId[i],BlackFideId[i],date[i],game_id,move[i].replace("\n", " "),round[i],event[i],Board[i],Result[i]))
          conn.commit()
      game_id+=1
