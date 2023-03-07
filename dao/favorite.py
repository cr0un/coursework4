from setup_db import db
from dao.model.favorite import Favorite

class FavoriteDAO:
    def __init__(self, session):
        self.session = session

    def add(self, favorite):
        self.session.add(favorite)
        self.session.commit()

    def get_by_user_and_movie(self, user_id, movie_id):
        return self.session.query(Favorite).filter_by(user_id=user_id, movie_id=movie_id).first()

    def delete(self, favorite):
        self.session.delete(favorite)
        self.session.commit()
