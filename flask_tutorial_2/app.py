from flask import Flask, render_template, request
import psycopg2


app = Flask(__name__)
transactions = []

def get_db_connection(): 
  conn = psycopg2.connect(host="localhost", dbname="DIS_test2_database", user="bjarkerasmusnicolaisen", 
                        port="5432")
  return conn
conn = get_db_connection()
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS transactions (date TEXT, amount REAL, account TEXT);")

conn.commit()
cur.close()
conn.close()

@app.route("/", methods=["GET","POST"])
def home():
  if request.method == "POST":
    print(request.form)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions VALUES (%s,%s,%s);", (
          request.form.get("date"),
          request.form.get("amount"),
          request.form.get("account"),
      ))
    conn.commit()
    cur.close()
    conn.close()
  return render_template("form.html")

@app.route("/transactions")
def show_transactions():
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM transactions;")
  transactions = cur.fetchall()
  conn.commit()
  cur.close()
  conn.close()
  return render_template("transactions.html", entries=transactions)




if __name__ == "__main__":
    app.run(debug=True) 