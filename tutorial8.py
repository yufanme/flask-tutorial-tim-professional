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
        found_user = User.query.filter_by(username=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = User(user, None)
            db.session.add(usr)
            db.session.commit()
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
            found_user = User.query.filter_by(username=user).first()
            found_user.email = email
            db.session.commit()
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


@app.route('/view')
def view():
    values = User.query.all()
    return render_template("view.html", values=values)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
