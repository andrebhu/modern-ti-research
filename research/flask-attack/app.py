#!/usr/bin/env python3

import base64
from flask import Flask, render_template, request, render_template_string, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "UNSAFE_SECRET"

@app.route("/")
def index():
    session["user"] = "admin"

    session_cookie = request.cookies["session"]
    decoded_session_cookie = b"".join(
        [base64.b64decode(f"{s}==".encode()) for s in session_cookie.split(".")]
    )

    return render_template(
        "index.html",
        session_cookie=session_cookie,
        decoded_session_cookie=decoded_session_cookie,
    )


if __name__ == "__main__":
    app.run(debug=True)
