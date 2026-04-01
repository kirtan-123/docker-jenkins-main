from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/about")
def about():
    return "This is deployed using Jenkins and Docker on AWS EC2"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
