setup database:
to setup the database, run the code in MakeDatabase.py in the main folder, which must contain the bund2324.pgn file.
before running MakeDatabase.py change PostgreSQL server info on line 44 and 60 in MakeDatabase.py and on line 5 in queries.py.

To run the web-app you should run the App.py file in a terminal and 
then enter "http://127.0.0.1:5000/" into a browser.

In the web-app, while not logged in you will have the option to search
for games in the database by inputting your desired search parameters. 
You will then get to see the results of the games that match the 
search parameters. You will also be able to register and log in. 
When registering, you should input a username, your password and your 
FIDE-ID. You can only register, if you are a player in the database and
no account is registered with your FIDE-ID. While searching when logged
in, you will also be able to see the moves from any game played by any
player in the same team as you. When logged in, you also have the 
additional option of uploading games (PGNs). You are only able to 
upload a game, if you are one of the players, who played that game,
base on FIDE-ID.
The database is initialized with one user, with the username "kim", 
the password "1234" and the FIDE-ID "1202758".
