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
WhiteFideId_pattern = re.compile("^\[WhiteFideId \"(.*)\"\]", re.MULTILINE)
BlackFideId_pattern = re.compile("^\[BlackFideId \"(.*)\"\]", re.MULTILINE)
WhiteTeam_pattern = re.compile("^\[WhiteTeam \"(.*)\"\]", re.MULTILINE)
BlackTeam_pattern = re.compile("^\[BlackTeam \"(.*)\"\]", re.MULTILINE)
Result_pattern = re.compile("^\[Result \"(.*)\"\]", re.MULTILINE)
move_pattern = re.compile("(^1\. [a-zA-Z0-9 \.+\n\/-]*)", re.MULTILINE)
Board_pattern = re.compile("^\[Board \"(.*)\"\]", re.MULTILINE)


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
    WhiteFideId = WhiteFideId_pattern.findall(tmp)
    BlackFideId = BlackFideId_pattern.findall(tmp)
    WhiteTeam = WhiteTeam_pattern.findall(tmp)
    BlackTeam = BlackTeam_pattern.findall(tmp)
    Result = Result_pattern.findall(tmp)
    move = move_pattern.findall(tmp)
    Board = Board_pattern.findall(tmp)

for elm in move:
    elm.replace("\n", "")

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
    name VARCHAR(255),
    elo VARCHAR(4),
    FideId VARCHAR(20) PRIMARY KEY)""")



cur.execute("""
    CREATE TABLE IF NOT EXISTS Teams (
    Team_name VARCHAR(255) PRIMARY KEY)""")

cur.execute("""
        CREATE TABLE IF NOT EXISTS PlayerTeams (
            FideId VARCHAR(255) REFERENCES Players(FideId),
            team_name VARCHAR(255) REFERENCES Teams(Team_name),
            PRIMARY KEY (FideId, team_name)
        )
    """)

cur.execute("""
    CREATE TABLE IF NOT EXISTS Leagues (
    Event VARCHAR(255) PRIMARY KEY)""")




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
            (black[i], whitelo[i], BlackFideId[i])
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

cur.execute("""
        CREATE TABLE IF NOT EXISTS League_Teams (
            Event VARCHAR(255) REFERENCES Leagues(Event),
            team_name VARCHAR(255) REFERENCES Teams(Team_name)
        )
    """)

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

cur.execute("""
        CREATE TABLE IF NOT EXISTS Team_match (
            Event VARCHAR(255) REFERENCES Leagues(Event),
            round VARCHAR(255),
            PRIMARY KEY (Event, round)
        )
    """)

for i in range(len(round)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Team_match WHERE Event = %s AND round = %s )", (event[i], round[i]))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute("INSERT INTO Team_match (Event, round) VALUES (%s, %s)", (event[i],round[i]))
        conn.commit()


cur.execute("""
        CREATE TABLE IF NOT EXISTS battle_in (
    Team_name VARCHAR(255) REFERENCES Teams(Team_name),
    Event VARCHAR(255),
    round VARCHAR(255),
    PRIMARY KEY (Team_name, Event, round),
    FOREIGN KEY (Event, round) REFERENCES Team_match(Event, round)
)
    """)

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


cur.execute("""
    CREATE TABLE IF NOT EXISTS Chessgame (
    white_player VARCHAR(255) REFERENCES Players(FideId),
    black_player VARCHAR(255) REFERENCES Players(FideId),   
    Date VARCHAR(255),
    game_id VARCHAR(255),
    moves VARCHAR,
    round VARCHAR(255),
    Event VARCHAR(255),
    board VARCHAR(255),
    result VARCHAR,
         
    PRIMARY KEY (white_player, black_player, game_id),
    FOREIGN KEY (Event, round) REFERENCES Team_match(Event, round)
)
    """)
game_id=1
for i in range(len(move)):
    cur.execute("SELECT EXISTS(SELECT 1 FROM Chessgame WHERE white_player = %s AND black_player = %s AND Event = %s AND round = %s)", (WhiteFideId[i], BlackFideId[i], event[i], round[i]))
    record_exists = cur.fetchone()[0]
    if not record_exists:
        cur.execute("INSERT INTO Chessgame (white_player, black_player, Date, game_id, moves, round, Event, board, result) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)", (WhiteFideId[i],BlackFideId[i],date[i],game_id,move[i].replace("\n", " "),round[i],event[i],Board[i],Result[i]))
        conn.commit()
    game_id+=1

cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR(255),
    password VARCHAR,
    FideId VARCHAR(20),
    PRIMARY KEY (username),
    FOREIGN KEY (FideId) REFERENCES Players(FideId))""")
cur.execute("INSERT INTO Users (username, password, FideId) VALUES (%s, %s, %s)", ("kim","1234", "1202758"))
conn.commit()
cur.close()
conn.close()