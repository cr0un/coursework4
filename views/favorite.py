from flask import g, request
from flask_restx import Namespace, Resource

from dao.favorite import FavoriteDAO
from decorators import auth_required
from service.auth import AuthService
from service.favorite import FavoriteService
from service.user import UserService
from setup_db import db

favorite_ns = Namespace("favorites", description="")


@favorite_ns.route('/movies/<int:movie_id>')
class FavoriteMovieView(Resource):

    @auth_required
    def post(self, movie_id):
        user_id = g.user.id
        access_token = request.headers.get('Authorization')
        refresh_token = request.headers.get('Refresh-Token')
        auth_service = AuthService(UserService())
        auth_service.check_valid_token(access_token=access_token.split(" ")[-1], refresh_token=refresh_token.split(" ")[-1])

        favorite_service = FavoriteService(FavoriteDAO())
        favorite_service.add_favorite_movie(user_id, movie_id)
        return "", 201, {"location": f"/movies/{movie_id}/favorite"}

    @auth_required
    def delete(self, movie_id):
        user_id = g.user.id
        favorite_service = FavoriteService(dao=FavoriteDAO(session=db.session))
        favorite_service.delete_favorite_movie(user_id, movie_id)
        return "", 204
