import psycopg2

conn = psycopg2.connect(host="localhost", dbname="DIS_test_database", user="bjarkerasmusnicolaisen", 
                        port="5432")

cur = conn.cursor()

# do something
cur.execute("""CREATE TABLE IF NOT EXISTS person (
  id INT PRIMARY KEY,
  name CHAR(100),
  age INT,
  gender CHAR
)
""" )

cur.execute("""
INSERT INTO person (id, name, age, gender) VALUES
            (1,'Mike',30,'M'), 
            (2,'Madonna',70,'F'),
            (3,'Nigel',68,'M'), 
            (4,'Ellen',6,'F')
""")

cur.execute(""" SELECT * FROM person WHERE gender = 'M';""")

print(cur.fetchone())

cur.execute(""" SELECT * FROM person WHERE age < 50; """)

for row in cur.fetchall():
  print(row)

conn.commit()

cur.close()
conn.close()