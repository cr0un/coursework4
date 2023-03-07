# from flask import request
# from flask_restx import Resource, Namespace
# from decorators import auth_required, admin_required
# from dao.model.movie import MovieSchema
# from implemented import movie_service
#
#
# movie_ns = Namespace('movies', description="API для фильмов")
#
#
# @movie_ns.route('/')
# class MoviesView(Resource):
#     @auth_required
#     def get(self):
#         director = request.args.get("director_id")
#         genre = request.args.get("genre_id")
#         year = request.args.get("year")
#         status = request.args.get("status")
#         page = request.args.get("page")
#
#
#         filters = {
#             "director_id": director,
#             "genre_id": genre,
#             "year": year,
#             "status": status,
#             "page": page
#         }
#         all_movies = movie_service.get_all(filters)
#         res = MovieSchema(many=True).dump(all_movies)
#         return res, 200
#
#     @admin_required
#     def post(self):
#         req_json = request.json
#         movie = movie_service.create(req_json)
#         return "", 201, {"location": f"/movies/{movie.id}"}
#
#
# @movie_ns.route('/<int:rid>')
# class MovieView(Resource):
#     @auth_required
#     def get(self, rid):
#         b = movie_service.get_one(rid)
#         sm_d = MovieSchema().dump(b)
#         return sm_d, 200
#
#     @admin_required
#     def put(self, rid):
#         req_json = request.json
#         if "id" not in req_json:
#             req_json["id"] = rid
#         movie_service.update(req_json)
#         return "", 204
#
#     @admin_required
#     def delete(self, rid):
#         movie_service.delete(rid)
#         return "", 204

from flask import request
from flask_restx import Resource, Namespace, fields

from decorators import auth_required, admin_required
from dao.model.movie import MovieSchema
from implemented import movie_service


movie_ns = Namespace('movies', description="API для фильмов")

# Описание моделей данных, используемых в запросах и ответах API.
movie_model = movie_ns.model('Movie', {
    'title': fields.String(required=True, description='Название фильма'),
    'year': fields.Integer(description='Год выпуска фильма'),
    'director_id': fields.Integer(description='Идентификатор режиссера фильма'),
    'genre_id': fields.Integer(description='Идентификатор жанра фильма'),
    'description': fields.Integer(description='Описание фильма')
})

# Добавление документации Swagger для MoviesView.
@movie_ns.route('/')
class MoviesView(Resource):
    @movie_ns.doc(description='Получение списка всех фильмов', security='jwt')
    @movie_ns.expect({
        'director_id': fields.Integer(description='Идентификатор режиссера фильма'),
        'genre_id': fields.Integer(description='Идентификатор жанра фильма'),
        'year': fields.Integer(description='Год выпуска фильма'),
        'page': fields.Integer(description='Номер страницы')
    })
    @movie_ns.response(200, 'Успешное получение списка фильмов')
    @auth_required
    def get(self):
        """
        Получение списка всех фильмов.
        """
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        page = request.args.get("page")

        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
            "page": page
        }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    @movie_ns.doc(description='Создание нового фильма', security='apikey')
    @movie_ns.expect(movie_model)
    @movie_ns.response(201, 'Успешное создание нового фильма')
    @movie_ns.response(401, 'Только для администраторов')
    @admin_required
    def post(self):
        """
        Создание нового фильма.
        """
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


# Добавление документации Swagger для MovieView.
@movie_ns.route('/<int:rid>')
class MovieView(Resource):
    @movie_ns.doc(description='Получение информации о фильме по идентификатору', security='jwt')
    @movie_ns.response(200, 'Успешное получение информации о фильме')
    @auth_required
    def get(self, rid):
        """
        Получение информации о фильме по идентификатору.
        """
        b = movie_service.get_one(rid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    @movie_ns.doc(description='Обновление информации о фильме', security='apikey')
    @movie_ns.expect(movie_model)
    @movie_ns.response(204, 'Успешное обновление информации о фильме')
    @movie_ns.response(401, 'Только для администраторов')
    @admin_required
    def put(self, rid):
        """
        Обновление информации о фильме.
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        movie_service.update(req_json)
        return "", 204

    @movie_ns.doc(description='Удаление информации о фильме', security='apikey')
    @movie_ns.response(204, 'Успешное удаление информации о фильме')
    @movie_ns.response(401, 'Только для администраторов')
    @admin_required
    def delete(self, rid):
        """
        Удаление информации о фильме по идентификатору.
        """
        movie_service.delete(rid)
        return "", 204
