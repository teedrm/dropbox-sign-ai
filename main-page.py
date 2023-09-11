from flask import Flask, render_template

app = Flask(__name__)

#future features check off
future_features = [
    {"name": "Live translation", "checked": False},
    {"name": "Read agreements aloud", "checked": False},
    {"name": "Auto-sign certain documents", "checked": False},
    {"name": "Remove signatures", "checked": False},
    {"name": "Manage document collections", "checked": False},
]

@app.route("/")
def home():
    return render_template("index.html", future_features=future_features)

if __name__ == "__main__":
    app.run(port=8080)