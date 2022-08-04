"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post
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



################### Routes for User #############################
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

    image_url = image_url if image_url else None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show information about a single user"""

    user = User.query.get_or_404(user_id)
    posts = user.posts


    return render_template("user-details.html", user = user, posts = posts)

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

################# Routes for Post #########################

@app.get("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show form for a new post"""

    user = User.query.get_or_404(user_id)

    return render_template("new-post-form.html",user = user)

@app.post("/users/<int:user_id>/posts/new")
def submit_new_post(user_id):
    """Submit a new post to the posts table return to user details page"""

    post_title = request.form["post-title"]
    post_content = request.form["post-content"]

    new_post = Post(title = post_title, content = post_content, user_id = user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def show_a_post(post_id):
    """Show an individual post"""

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template("post-details.html", post = post, user = user)


@app.get("/posts/<int:post_id>/edit")
def show_edit_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template("post-edit.html", post = post, user = user )


@app.post("/posts/<int:post_id>/edit")
def update_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form["post-title"]
    post.content = request.form["post-content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete a post"""

    post = Post.query.get_or_404(post_id)
    user = post.user
    db.session.delete(post)
    db.session.commit()

    flash("Post Deleted")

    return redirect(f"/users/{user.id}")
