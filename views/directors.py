# from flask import request
# from flask_restx import Resource, Namespace
# from decorators import auth_required, admin_required
# from dao.model.director import DirectorSchema
# from implemented import director_service
#
# director_ns = Namespace('directors', description="API для режиссеров")
#
#
# @director_ns.route('/')
# class DirectorsView(Resource):
#     @auth_required
#     def get(self):
#         page = request.args.get("page")
#         filters = {
#             "page": page
#         }
#         rs = director_service.get_all(filters)
#         res = DirectorSchema(many=True).dump(rs)
#         return res, 200
#
#     @admin_required
#     def post(self):
#         req_json = request.json
#         director = director_service.create(req_json)
#         return "", 201, {"location": f"/directors/{director.id}"}
#
#
# @director_ns.route('/<int:rid>')
# class DirectorView(Resource):
#     @auth_required
#     def get(self, rid):
#         r = director_service.get_one(rid)
#         sm_d = DirectorSchema().dump(r)
#         return sm_d, 200
#
#     @admin_required
#     def put(self, rid):
#         req_json = request.json
#         if "id" not in req_json:
#             req_json["id"] = rid
#         director_service.update(req_json)
#         return "", 204
#
#     @admin_required
#     def delete(self, rid):
#         director_service.delete(rid)
#         return "", 204

from flask import request
from flask_restx import Resource, Namespace, fields

from decorators import auth_required, admin_required
from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors', description="API для режиссеров")

# Описание моделей данных, используемых в запросах и ответах API.
director_model = director_ns.model('Director', {
    'id': fields.String(required=True, description='id'),
    'name': fields.String(required=True, description='Имя режиссера')
})

# Добавление документации Swagger для DirectorsView.
@director_ns.route('/')
class DirectorsView(Resource):
    @director_ns.doc(description='Получение списка всех режиссеров', security='apikey')
    @director_ns.response(200, 'Успешное получение списка режиссеров')
    @auth_required
    def get(self):
        """
        Получение списка всех режиссеров.
        """
        page = request.args.get("page")
        filters = {
            "page": page
        }
        rs = director_service.get_all(filters)
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @director_ns.doc(description='Создание нового режиссера', security='apikey')
    @director_ns.expect(director_model)
    @director_ns.response(201, 'Успешное создание нового режиссера')
    @director_ns.response(401, 'Только для администраторов')
    @admin_required
    def post(self):
        """
        Создание нового режиссера.
        """
        req_json = request.json
        director = director_service.create(req_json)
        return "", 201, {"location": f"/directors/{director.id}"}


# Добавление документации Swagger для DirectorView.
@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @director_ns.doc(description='Получение информации о режиссере по идентификатору', security='apikey')
    @director_ns.response(200, 'Успешное получение информации о режиссере')
    @auth_required
    def get(self, rid):
        """
        Получение информации о режиссере по идентификатору.
        """
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @director_ns.doc(description='Обновление информации о режиссере', security='apikey')
    @director_ns.expect(director_model)
    @director_ns.response(204, 'Успешное обновление информации о режиссере')
    @director_ns.response(401, 'Только для администраторов')
    @admin_required
    def put(self, rid):
        """
        Обновление информации о режиссере по идентификатору.
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        director_service.update(req_json)
        return "", 204


    @director_ns.doc(description='Удаление режиссера по его ID', security='jwt')
    @director_ns.response(204, 'Режиссер удален успешно')
    @admin_required
    def delete(self, rid):
        """
        Удаление режиссера по его ID.
        """
        director_service.delete(rid)
        return "", 204

