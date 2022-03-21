# flash a message
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "FAN"
app.permanent_session_lifetime = timedelta(seconds=20)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __init__(self, username, email):
        self.username = username
        self.email = email



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        session.permanent = True
        session["user"] = user
        flash("Login success!", "info")
        return redirect(url_for("userinfo"))
    else:
        if "user" in session:
            flash("Already log in!")
            return redirect(url_for("userinfo"))
        return render_template("login.html")


@app.route("/userinfo", methods=["GET", "POST"])
def userinfo():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("userinfo.html", user=user, email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"you have been logged out {user}.", "info")
        session.pop("user", None)
        session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
