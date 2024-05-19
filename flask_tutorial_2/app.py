from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
  print(request.form.get("amount"))
  return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True) 