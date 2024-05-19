from flask import Flask, render_template, request

app = Flask(__name__)
transactions = [
   ("2024-05-19",70.00,"Checking"),
   ("2024-05-21",150.00,"Savings"),
   ("2024-05-23",15.96,"Checking"),
]


@app.route("/", methods=["GET","POST"])
def home():
  if request.method == "POST":
    print(request.form)
    transactions.append(
      (
          request.form.get("date"),
          request.form.get("amount"),
          request.form.get("account"),
      )
    )
  return render_template("form.html")

@app.route("/transactions")
def show_transactions():
  return render_template("transactions.html", entries=transactions)




if __name__ == "__main__":
    app.run(debug=True) 