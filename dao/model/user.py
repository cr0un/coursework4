from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    change_password = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    surname = db.Column(db.String(255), nullable=True)
    favorite_genre = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True)
    genre = db.relationship("Genre")


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()
    # password = fields.Str(load=True)
    # change_password = fields.Str(load=True)
    # role = fields.Str(load=True)
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()

