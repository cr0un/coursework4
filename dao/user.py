from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, rid):
        return self.session.query(User).get(rid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        user = User(**user_d)
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user):
        user_db = self.get_one(user.id)
        user_db.name = user.name
        user_db.surname = user.surname
        user_db.favorite_genre = user.favorite_genre
        self.session.commit()

    def get_by_username(self, email):
        return self.session.query(User).filter(User.email == email).first()
