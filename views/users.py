from flask_restx import Resource, Namespace, fields
from flask import request

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users', description="API для пользователей")


# @user_ns.route('/')
# class UserView(Resource):
#     def get(self):
#         rs = user_service.get_all()
#         res = UserSchema(many=True).dump(rs)
#         return res, 200
#
#     def post(self):
#         req_json = request.json
#         user = user_service.create(req_json)
#         return "", 201, {"location": f"/users/{user.id}"}
#
#
# @user_ns.route('/<int:rid>')
# class UserView(Resource):
#     def get(self, rid):
#         r = user_service.get_one(rid)
#         sm_d = UserSchema().dump(r)
#         return sm_d, 200
#
#     def patch(self, rid):
#         req_json = request.json
#         if "id" not in req_json:
#             req_json["id"] = rid
#         user_service.update(req_json)
#         return "", 204
#
#     def delete(self, rid):
#         user_service.delete(rid)
#         return "", 204
#
# @user_ns.route("/password")
# class UpdateUserPassViews(Resource):
#     def put(self):
#         req_json = request.json
#         email = req_json.get("email")
#         old_pass = req_json.get("password_1")
#         new_pass = req_json.get("password_2")
#         user = user_service.get_by_email(email)
#         if user_service.compare_passwords(user.password, old_pass):
#             user.password = user_service.get_hash(new_pass)
#             result = UserSchema().dump(user)
#             user_service.update(result)
#         else:
#             print("Error, password didnt changed")
#         return "", 201

# определяем модели для документирования
user_model = user_ns.model('User', {
    'email': fields.String(required=True, description='Email пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя'),
})

user_password_model = user_ns.model('UserPassword', {
    'email': fields.String(required=True, description='Email пользователя'),
    'password_1': fields.String(required=True, description='Старый пароль пользователя'),
    'password_2': fields.String(required=True, description='Новый пароль пользователя'),
})


# Добавление документации Swagger для UserView.
@user_ns.route('/')
class UserListView(Resource):
    @user_ns.doc(description='Получение списка всех пользователей', security='jwt')
    @user_ns.response(200, 'Успешное получение списка всех пользователей')
    def get(self):
        """
        Получение списка всех пользователей.
        """
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    @user_ns.doc(description='Создание нового пользователя', security='apikey')
    @user_ns.expect(user_model)
    @user_ns.response(201, 'Успешное создание нового пользователя')
    @user_ns.response(401, 'Только для администраторов')
    def post(self):
        """
        Создание нового пользователя.
        """
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:rid>')
class UserView(Resource):
    @user_ns.doc(description='Получение информации о пользователе по идентификатору', security='jwt')
    @user_ns.response(200, 'Успешное получение информации о пользователе по идентификатору')
    def get(self, rid):
        """
        Получение информации о пользователе по идентификатору.
        """
        r = user_service.get_one(rid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    @user_ns.doc(description='Частичное обновление информации о пользователе', security='apikey')
    @user_ns.expect(user_model)
    @user_ns.response(204, 'Успешное частичное обновление информации о пользователе')
    @user_ns.response(401, 'Только для администраторов')
    def patch(self, rid):
        """
        Частичное обновление информации о пользователе.
        """
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        user_service.update(req_json)
        return "", 204

    @user_ns.doc(description='Удаление информации о пользователе', security='apikey')
    @user_ns.response(204, 'Успешное удаление информации о пользователе')
    @user_ns.response(401, 'Только для администраторов')
    def delete(self, rid):
        """
        Удаление информации о пользователе по идентификатору.
        """
        user_service.delete(rid)
        return "", 204


@user_ns.route("/password")
class UpdateUserPassViews(Resource):
    @user_ns.doc(description='Обновление пароля пользователя', security='jwt')
    @user_ns.expect(user_password_model)
    @user_ns.response(201, 'Успешное обновление пароля пользователя')
    def put(self):
        """
        Обновление пароля пользователя.
        """
        req_json = request.json
        email = req_json.get("email")
        old_pass = req_json.get("password_1")
        new_pass = req_json.get("password_2")
        user = user_service.get_by_email(email)
        if user_service.compare_passwords(user.password, old_pass):
            user.password = user_service.get_hash(new_pass)
            result = UserSchema().dump(user)
            user_service.update(result)
        else:
            print("Error, password didnt changed")
        return "", 201

