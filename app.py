from __future__ import print_function
import logging
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

# Configure SQL database
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


@app.route("/form", methods=["GET","POST"])
def form():
    if request.method == "POST":
        
        # If any fields are blank
        if not request.form.get("social") or not request.form.get("workload") or not request.form.get("comp") or not request.form.get("comment"):
            return redirect("/form")
        
        # Check if user has already submitted review
        user = session["user_id"]
        if len(cursor.execute("SELECT user FROM reviews WHERE user = ? AND club = ?", (user, request.form.get("club"))).fetchall()) > 0:
            cursor.execute("UPDATE reviews set social = ?, workload = ?, comp = ?, comment = ? WHERE user = ? AND club = ?",
            (request.form.get("social"), request.form.get("workload"), request.form.get("comp"), request.form.get("comment"), user, request.form.get("club")))
            connect.commit()
            
        else:
            try:
                cursor.execute("INSERT INTO reviews (user, social, workload, comp, comment, club) VALUES (?, ?, ?, ?, ?, ?)", 
                    (user, request.form.get("social"), request.form.get("workload"), 
                    request.form.get("social"), request.form.get("comment"), request.form.get("club")))
                connect.commit()
            except ValueError:
                return redirect("/form")
        return redirect("/review")
    else:
        return render_template("form.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get users
        users = cursor.execute("SELECT username FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        
        # If user doesn't exist
        if len(users) != 1:
            flash("User does not exist", "error")
            return redirect("/login")
        hash = cursor.execute("SELECT hash FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()[0]
        
        # If password is wrong
        if not check_password_hash(hash, request.form.get("password")):
            flash("Incorrect password")
            return redirect("/login")
        session["user_id"] = users[0][0]
        return redirect("/homepage")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # All fields are filled
        if not request.form.get("username") or not request.form.get("password"):
            flash("Missing fields")
            return redirect("/register")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match")
            return redirect("/register")
        
        # Make sure it's a harvard email
        if not "@college.harvard.edu" in request.form.get("email"):
            flash("Must be a Harvard College email")
            return redirect("/register")

        if len(cursor.execute("SELECT email FROM users WHERE email = ?",
                            (request.form.get("email"),)).fetchall()) > 0:
            flash("Email is taken")
            return redirect("/register")

        # If username is taken
        if len(cursor.execute("SELECT username FROM users WHERE username = ?",
                            (request.form.get("username"),)).fetchall()) > 0:
            flash("Username is taken")
            return redirect("/register")
        try:
            # Add users
            cursor.execute("INSERT INTO users (email, username, hash) VALUES(?, ?, ?)",
                            (request.form.get("email"), request.form.get("username"),
                            generate_password_hash(request.form.get("password"))))
            connect.commit()
            return redirect("/login")
        except ValueError:
            return render_template("register.html")
    return render_template("register.html")


@app.route('/review', methods=["GET", "POST"])
def review():
    if request.method == 'POST':
        club = request.form.get("club")

        return render_template("form.html", club=club)
    
    return render_template("review.html", clubdata=zip(get_clubs(), get_images()))


@app.route('/theq', methods=["GET", "POST"])
def theq():
    if request.method == 'POST':
        club = request.form.get("theq")
        reviews = cursor.execute("SELECT AVG(social) as social, AVG(workload) as workload, AVG(comp) as comp FROM reviews WHERE club == ?", (club,)).fetchall()[0]
        comments = cursor.execute("SELECT comment as comments FROM reviews WHERE club == ?", (club,)).fetchall()
        if not reviews or not comments:
            reviews = []
            comments = []
        return render_template("theq.html", club=club, reviews=reviews, comments=comments)
    return render_template("theq.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")