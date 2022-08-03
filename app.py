"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_users():

    return redirect("/users")


@app.get("/users")
def show_users():

    return render_template("users-listing.html")

@app.get("users/new")
def show_add_form():

    return render_template("new-user-form.html")

@app.post("/users/new")
def add_user():

    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    image_url = request.form.get("img")

    new_user = User(first_name, last_name, image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int: user_id>")
def show_user_detail(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("user-details.html", user = user)








