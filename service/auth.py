from constants import JWT_ALGO, JWT_SECRET_KEY
import datetime
import calendar
import jwt
from service.user import UserService

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)
        if user is None:
            raise Exception()

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                raise Exception()

        data = {
            "email": user.email,
            "role": user.role
        }

        access_token_lifetime = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(access_token_lifetime.timetuple())
        access_token = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGO)

        refresh_token_lifetime = datetime.datetime.utcnow() + datetime.timedelta(days=180)
        data["exp"] = calendar.timegm(refresh_token_lifetime.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGO)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def check_token_refresh(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGO, ])
        email = data.get("email")

        user = self.user_service.get_by_email(email)

        if user is None:
            raise Exception()
        return self.generate_token(email, user.password, is_refresh=True)

    def check_valid_token(self, access_token, refresh_token):
        try:
            jwt.decode(jwt=access_token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGO])
            jwt.decode(jwt=refresh_token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGO])
        except Exception as e:
            return False

        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGO])
        email = data.get("email")

        user = self.user_service.get_by_email(email)

        if user is None:
            raise Exception()

        return self.generate_token(user.email, user.password, is_refresh=True)
