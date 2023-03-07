import hashlib
import base64
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.get_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def update(self, user_d):
        user_id = user_d.get("id")
        user = self.get_one(user_id)

        if user is None:
            raise ValueError(f"User with ID {user_id} not found.")

        fields_to_update = ["name", "surname", "favorite_genre"]

        for field in fields_to_update:
            if user_d.get(field):
                setattr(user, field, user_d.get(field))

        user.password = self.get_hash(user.password) if user.password else user.password

        self.dao.update(user)

    def delete(self, rid):
        self.dao.delete(rid)

    def get_by_email(self, email):
        return self.dao.get_by_username(email)

    def get_hash(self, password):
        if isinstance(password, bytes):
            return base64.b64encode(hashlib.pbkdf2_hmac(
                'sha256',
                password,  # password is already bytes
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            ))
        else:
            return base64.b64encode(hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),  # Convert the password to bytes
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            ))

    def compare_passwords(self, password_hash, request_password):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac('sha256',
            request_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS)
        )

