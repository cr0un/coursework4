from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, rid):
        return self.dao.get_one(rid)

    def get_all(self, filter):
        return self.dao.get_all(filter)

    def create(self, genre_d):
        return self.dao.create(genre_d)

    def update(self, genre_d):
        self.dao.update(genre_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
