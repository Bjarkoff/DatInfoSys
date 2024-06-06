setup database:
to setup the database, run the code in MakeDatabase.py in the main folder, which must contain the bund2324.pgn file.
before running MakeDatabase.py change PostgreSQL server info on line 44 and 60 in MakeDatabase.py and on line 5 in queries.py.

To run the web-app you should run the App.py file in a terminal and 
then enter "http://127.0.0.1:5000/" into a browser.

The project is a database over team matches in chess. 
The idea is to allow users, who are not logged in, to 
search the database, however when not logged in the user
is not allowed to see actual moves of the games played 
(since this information contains valuable information
about players' styles and habits).

To login, one has to be a user already in the database,
or register. The database is initialized with one user, 
with the username "kim", the password "1234" and the FIDE-ID "1202758".
To register a new user, one has to choose a username that has not been used,
a password, and a fideID which is both registered with an existing 
player in the database, and not registered with an existing user.
The validation of the new user exists then only in the knowledge
of a relevant fideID.

Once logged in, the user can search the database as before,
however while searching when logged in the user will also be able 
to see the moves from any game played by any
player in the same team as the user. When logged in, the user also has the 
additional option of uploading games (PGNs). You are only able to 
upload a game, if you are one of the players, who played that game,
based on FIDE-ID.

