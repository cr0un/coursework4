# from flask import request
# from flask_restx import Resource, Namespace
# from decorators import auth_required, admin_required
# from dao.model.genre import GenreSchema
# from implemented import genre_service
#
# genre_ns = Namespace('genres', description="API для жанров")
#
#
# @genre_ns.route('/')
# class GenresView(Resource):
#     @auth_required
#     def get(self):
#         page = request.args.get("page")
#
#         filters = {
#             "page": page
#         }
#         rs = genre_service.get_all(filters)
#         res = GenreSchema(many=True).dump(rs)
#         return res, 200
#
#
#     @admin_required
#     def post(self):
#         req_json = request.json
#         genre = genre_service.create(req_json)
#         return "", 201, {"location": f"/genres/{genre.id}"}
#
#
# @genre_ns.route('/<int:rid>')
# class GenreView(Resource):
#     @auth_required
#     def get(self, rid):
#         r = genre_service.get_one(rid)
#         sm_d = GenreSchema().dump(r)
#         return sm_d, 200
#
#     # def get(self):
#     #     page = request.args.get("page")
#     #     filters = {
#     #         "page": page
#     #     }
#     #     rs = genre_service.get_all(filters)  # передаем фильтры как аргумент метода
#     #     res = GenreSchema(many=True).dump(rs)
#     #     return res, 200
#
#     @admin_required
#     def put(self, rid):
#         req_json = request.json
#         if "id" not in req_json:
#             req_json["id"] = rid
#         genre_service.update(req_json)
#         return "", 204
#
#     @admin_required
#     def delete(self, rid):
#         genre_service.delete(rid)
#         return "", 204

from flask import request
from flask_restx import Resource, Namespace, fields

from decorators import auth_required, admin_required
from dao.model.genre import GenreSchema
from implemented import genre_service

genre_ns = Namespace('genres', description="API для жанров")

# Описание моделей данных, используемых в запросах и ответах API.
genre_model = genre_ns.model('Genre', {
    'id': fields.String(required=True, description='id'),
    'name': fields.String(required=True, description='Название жанра')
})


# Добавление документации Swagger для GenresView.
@genre_ns.route('/')
class GenresView(Resource):
    @genre_ns.doc(description='Получение списка всех жанров', security='jwt')
    @genre_ns.response(200, 'Успешное получение списка жанров')
    @auth_required
    def get(self):
        """
        Получение списка всех жанров.
        """
        page = request.args.get("page")

        filters = {
            "page": page
        }
        rs = genre_service.get_all(filters)
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @genre_ns.doc(description='Создание нового жанра', security='apikey')
    @genre_ns.expect(genre_model)
    @genre_ns.response(201, 'Успешное создание нового жанра')
    @genre_ns.response(401, 'Только для администраторов')
    @admin_required
    def post(self):
        """
        Создание нового жанра.
        """
        req_json = request.json
        genre = genre_service.create(req_json)
        return "", 201, {"location": f"/genres/{genre.id}"}


# Добавление документации Swagger для GenreView.
@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @genre_ns.doc(description='Получение информации о жанре по идентификатору', security='jwt')
    @genre_ns.response(200, 'Успешное получение информации о жанре')
    @auth_required
    def get(self, rid):
        """
        Получение информации о жанре по идентификатору.
        """
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @genre_ns.doc(description='Обновление информации о жанре', security='apikey')
    @genre_ns.expect(genre_model)
    @genre_ns.response(204, 'Успешное обновление информации о жанре')
    @genre_ns.response(401, 'Только для администраторов')
    @admin_required
    def put(self, rid):
        """
        Обновление информации о жанре по идентификатору.
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        genre_service.update(req_json)
        return "", 204

    @genre_ns.doc(description='Удаление информации о жанре', security='apikey')
    @genre_ns.response(204, 'Успешное удаление информации о жанре')
    @genre_ns.response(401, 'Только для администраторов')
    @admin_required
    def delete(self, rid):
        """
        Удаление информации о жанре по идентификатору.
        """
        genre_service.delete(rid)
        return "", 204
