from marshmallow import Schema, fields
from setup_db import db


class Favorite(db.Model):
    __tablename__ = 'favorite'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    user = db.relationship("User")
    movie = db.relationship("Movie")

class FavoriteMovieSchema(Schema):
    user_id = fields.Int()
    movie_id = fields.Int()
