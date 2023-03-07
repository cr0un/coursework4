from dao.model.favorite import Favorite
from dao.favorite import FavoriteDAO

class FavoriteService:
    def __init__(self, dao):
        self.favorite_dao = dao

    def add_favorite_movie(self, user_id, movie_id):
        favorite = Favorite(user_id=user_id, movie_id=movie_id)
        self.favorite_dao.add(favorite)
        return favorite

    def delete_favorite_movie(self, user_id, movie_id):
        favorite = self.favorite_dao.get_by_user_and_movie(user_id, movie_id)
        if not favorite:
            return None
        self.favorite_dao.delete(favorite)
        return favorite
