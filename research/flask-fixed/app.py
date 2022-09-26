#!/usr/bin/env python3

from flask import Flask, render_template, request, session # importing Flask's builtin session

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersafesecretkey" # not a safe secret key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["user"] = "visitor" # everyone is assigned to visitor
        data = request.form["input"]

        return render_template(
            "index.html", 
            data=data, 
            user=session["user"] # retrieving "user" cookie
        )
    return render_template("index.html", user=session["user"])

if __name__ == "__main__":
    app.run()