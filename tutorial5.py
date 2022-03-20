from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "FAN"
app.permanent_session_lifetime = timedelta(seconds=20)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        session.permanent = True
        session["user"] = user
        return redirect(url_for("userinfo"))
    else:
        if "user" in session:
            return redirect(url_for("userinfo"))
        return render_template("login.html")


@app.route("/userinfo")
def userinfo():
    if "user" in session:
        return f"<h1>{session['user']}'s personal page.</h1>"
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
