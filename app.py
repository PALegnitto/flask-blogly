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

