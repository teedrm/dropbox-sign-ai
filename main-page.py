from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/template")
def templates():
    return "template"

if __name__ == "__main__":
    app.run(port=8080)