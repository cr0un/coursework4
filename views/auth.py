# from flask import request
# from flask_restx import Resource, Namespace
#
# from implemented import auth_service, user_service
#
# auth_ns = Namespace("auth")
#
# @auth_ns.route("/register")
# class RegisterView(Resource):
#     def post(self):
#         req_json = request.json
#         email = req_json.get("email")
#         password = req_json.get("password")
#
#         if None in [email, password]:
#             return "", 401
#
#         # req_json["favorite_genre"] = 1
#         user_service.create(req_json)
#         return "User created successfully", 201
#
#
# @auth_ns.route("/login")
# class LoginView(Resource):
#     def post(self):
#         req_json = request.json
#         email = req_json.get("email")
#         password = req_json.get("password")
#
#         if None in [email, password]:
#             return "", 401
#
#         tokens = auth_service.generate_token(email, password)
#         return tokens, 201
#
#     def put(self):
#         req_json = request.json
#         access_token = req_json.get("access_token")
#         refresh_token = req_json.get("refresh_token")
#
#         if None in [access_token, refresh_token]:
#             return "", 401
#
#         tokens = auth_service.check_valid_token(access_token, refresh_token)
#         return tokens, 201
#

from flask import request
from flask_restx import Resource, Namespace, fields

from implemented import auth_service, user_service

auth_ns = Namespace("auth", description="API для авторизации")

# Описание моделей данных, используемых в запросах и ответах API.
user_model = auth_ns.model('User', {
    'email': fields.String(required=True, description='Email пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя')
})

token_model = auth_ns.model('Token', {
    'access_token': fields.String(required=True, description='JWT-токен доступа'),
    'refresh_token': fields.String(required=True, description='JWT-токен обновления')
})

# Добавление документации Swagger для RegisterView.
@auth_ns.route("/register")
class RegisterView(Resource):
    @auth_ns.doc(description='Регистрация нового пользователя', security=None)
    @auth_ns.expect(user_model)
    @auth_ns.response(201, 'Успешная регистрация пользователя')
    @auth_ns.response(401, 'Некорректные данные пользователя')
    def post(self):
        """
        Создание нового пользователя в системе.
        """
        req_json = request.json
        email = req_json.get("email")
        password = req_json.get("password")

        if None in [email, password]:
            return "", 401

        # req_json["favorite_genre"] = 1
        user_service.create(req_json)
        return "User created successfully", 201


# Добавление документации Swagger для LoginView.
@auth_ns.route("/login")
class LoginView(Resource):
    @auth_ns.doc(description='Аутентификация пользователя', security=None)
    @auth_ns.expect(user_model)
    @auth_ns.response(201, 'Успешная аутентификация')
    @auth_ns.response(401, 'Некорректные данные пользователя')
    def post(self):
        """
        Получение JWT-токенов доступа и обновления для пользователя.
        """
        req_json = request.json
        email = req_json.get("email")
        password = req_json.get("password")

        if None in [email, password]:
            return "", 401

        tokens = auth_service.generate_token(email, password)
        return tokens, 201

    @auth_ns.doc(description='Обновление JWT-токенов доступа и обновления', security=None)
    @auth_ns.expect(token_model)
    @auth_ns.response(201, 'Токены обновлены успешно')
    @auth_ns.response(401, 'Некорректные данные токенов')
    def put(self):
        """
        Обновление JWT-токенов доступа и обновления для пользователя.
        """
        req_json = request.json
        access_token = req_json.get("access_token")
        refresh_token = req_json.get("refresh_token")

        if None in [access_token, refresh_token]:
            return "", 401

        tokens = auth_service.check_valid_token(access_token, refresh_token)
        return tokens, 201
