from __future__ import print_function
import os
import jinja2
import sys


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


import sqlite3
from PIL import Image
import os

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


connect = sqlite3.connect("project.db", check_same_thread=False)
cursor = connect.cursor()
def get_clubs():
    clubs = cursor.execute("SELECT name FROM clubs")
    return clubs.fetchall()
def get_images():
    images = cursor.execute("SELECT logo FROM clubs")
    return images.fetchall()


@app.route("/homepage")
def homepage():
    return render_template("homepage.html", clubdata=zip(get_clubs(), get_images()))


@app.route("/")
def open():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = cursor.execute("SELECT username FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        print(users, file=sys.stderr)
        if len(users) != 1:
            return render_template("login.html")
        hash = cursor.execute("SELECT hash FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()[0]
        if not check_password_hash(hash, request.form.get("password")):
            return render_template("login.html")
        session["user_id"] = users[0][0]
        return redirect("/homepage")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return redirect("/register")
            # return render_template("login.html")
        elif not request.form.get("password"):
            return redirect("/register")
            # return render_template("login.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            return redirect("/register")
            # return render_template("login.html")
        if not "@college.harvard.edu" in request.form.get("email"):
            return redirect("/register")
            # return render_template("login.html")
        
        try:
            cursor.execute("INSERT INTO users (email, username, hash) VALUES(?, ?, ?)",
                            (request.form.get("email"), request.form.get("username"),
                            generate_password_hash(request.form.get("password"))))
            connect.commit()
        except ValueError:
            return redirect("/register")
    return render_template("login.html")


@app.route('/review', methods=["GET", "POST"])
def review():
    
    return render_template("review.html")


# @app.route('/history')
# def history():
#     return render_template("history.html")


@app.route('/theq')
def theq():
    return render_template("theq.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")