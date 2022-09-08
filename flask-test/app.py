#!/usr/bin/env python3

from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "p1": request.form["input"],
            "p2": render_template_string(request.form["input"])
        }
        return render_template("index.html", data=data)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)