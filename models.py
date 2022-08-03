"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    # can specify multi-column unique or check constraints like:
   # __table_args__ = (
   #    db.UniqueConstraint("col1", "col2"),
   #    db.CheckConstraint("born <= died") )
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
            db.String(50), nullable=False
            )

    last_name = db.Column(
            db.String(50), nullable=False
            )

    image_url = db.Column(
            db.Text
            )
