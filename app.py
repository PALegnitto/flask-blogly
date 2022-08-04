"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "hunter2"

app.debug = True
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_users():
    """Redirects to user listing"""

    return redirect("/users")


@app.get("/users")
def show_users():
    """Shows a list of users in database"""

    users = User.query.all()

    return render_template("users-listing.html", users = users)

@app.get("/users/new")
def show_add_form():
    """Show form to add a new user"""

    return render_template("new-user-form.html")

@app.post("/users/new")
def add_user():
    """Add user to database and redirect to user list"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["img"]

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show information about a single user"""

    user = User.query.get_or_404(user_id)

    return render_template("user-details.html", user = user)

@app.get("/users/<int:user_id>/edit")
def show_user_edit(user_id):
    """Show form to edit user information"""

    user = User.query.get_or_404(user_id)

    return render_template("user-edit.html", user = user)


@app.post("/users/<int:user_id>/edit")
def perform_user_edit(user_id):
    """Update user information and redirect to user page"""

    user = User.query.get(user_id)

    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["img"]

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.post("/users/<int:user_id>/delete")
def perform_user_delete(user_id):
    """Delete user and return to user listing"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash("User Deleted")

    return redirect("/users")


