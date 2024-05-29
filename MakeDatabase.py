import psycopg2
from psycopg2 import sql
import re

Event_pattern = re.compile("^\[Event \"(.*)\"\]", re.MULTILINE)
Date_pattern = re.compile("^\[Date \"(.*)\"\]", re.MULTILINE)
Round_pattern = re.compile("^\[Round \"(.*)\"\]", re.MULTILINE)
White_pattern = re.compile("^\[White \"(.*)\"\]", re.MULTILINE)
Black_pattern = re.compile("^\[Black \"(.*)\"\]", re.MULTILINE)
WhiteElo_pattern = re.compile("^\[WhiteElo \"(.*)\"\]", re.MULTILINE)
BlackElo_pattern = re.compile("^\[BlackElo \"(.*)\"\]", re.MULTILINE)
WhiteTeam_pattern = re.compile("^\[WhiteTeam \"(.*)\"\]", re.MULTILINE)
BlackTeam_pattern = re.compile("^\[BlackTeam \"(.*)\"\]", re.MULTILINE)
Result_pattern = re.compile("^\[Result \"(.*)\"\]", re.MULTILINE)
move_pattern = re.compile("(^1\. [a-zA-Z0-9 \.+\n\/-]*)", re.MULTILINE)


with open('bund2324.pgn', 'r') as textfile:
    tmp =textfile.read()
    event = Event_pattern.findall(tmp)
    date = Date_pattern.findall(tmp)
    round = Round_pattern.findall(tmp)
    move = move_pattern.findall(tmp)
    white = White_pattern.findall(tmp)
    black = Black_pattern.findall(tmp)
    whitelo = WhiteElo_pattern.findall(tmp)
    BlackElo = BlackElo_pattern.findall(tmp)
    WhiteTeam = WhiteTeam_pattern.findall(tmp)
    BlackTeam = BlackTeam_pattern.findall(tmp)
    Result = Result_pattern.findall(tmp)
    move = move_pattern.findall(tmp)



# Connect to the PostgreSQL server
conn = psycopg2.connect(
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
conn.autocommit = True  
cur = conn.cursor()
new_database_name = "teamchess"
cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(new_database_name)))

cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_database_name)))

cur.close()
conn.close()

conn = psycopg2.connect(
    dbname="teamchess",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
    )
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS Players (
    name VARCHAR(255) PRIMARY KEY,
    elo VARCHAR(4))""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Teams (
    name VARCHAR(255) PRIMARY KEY)""")

cur.execute("""
        CREATE TABLE IF NOT EXISTS PlayerTeams (
            player_name VARCHAR(255) REFERENCES Players(name),
            team_name VARCHAR(255) REFERENCES Teams(name),
            PRIMARY KEY (player_name, team_name)
        )
    """)

for i in range(len(white)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Players WHERE name = %s)", (white[i],))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute(
            sql.SQL("INSERT INTO Players (name, elo) VALUES (%s, %s)"),
            (white[i], whitelo[i])
        )
        conn.commit()

for i in range(len(black)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Players WHERE name = %s)", (black[i],))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute(
            sql.SQL("INSERT INTO Players (name, elo) VALUES (%s, %s)"),
            (black[i], whitelo[i])
        )
        conn.commit()

for i in range(len(WhiteTeam)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Teams WHERE name = %s)", (WhiteTeam[i],))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute("INSERT INTO Teams (name) VALUES (%s)", (WhiteTeam[i],))
        conn.commit()

for i in range(len(BlackTeam)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Teams WHERE name = %s)", (BlackTeam[i],))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute("INSERT INTO Teams (name) VALUES (%s)", (WhiteTeam[i],))
        conn.commit()

for i in range(len(white)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM PlayerTeams WHERE player_name = %s AND team_name = %s)", (white[i], WhiteTeam[i]))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute("INSERT INTO PlayerTeams (player_name, team_name) VALUES (%s, %s)", (white[i],WhiteTeam[i]))
        conn.commit()

for i in range(len(black)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM PlayerTeams WHERE player_name = %s AND team_name = %s)", (black[i], BlackTeam[i]))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute("INSERT INTO PlayerTeams (player_name, team_name) VALUES (%s, %s)", (black[i],BlackTeam[i]))
        conn.commit()

cur.close()
conn.close()