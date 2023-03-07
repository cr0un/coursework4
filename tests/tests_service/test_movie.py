import pytest

from service.movie import MovieService

class TestMovieService:

    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_all(self):
        genres = self.movie_service.get_all({})
        assert genres is not None
        assert len(genres) > 0

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None
        assert movie.title == "Movie_1"

    def test_create(self):
        movie_d = {
            "title": "Movie 5",
            "description": "my_description",
            "trailer": "link",
            "year": 1999,
            "rating": 9.0,
            "genre_id": 1,
            "director_id": 1
        }

        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_update(self):
        movie_d = {
            "id": 1,
            "title": "The Movie 5",
            "description": "my_description",
            "trailer": "link",
            "year": 1999,
            "rating": 9.0,
            "genre_id": 1,
            "director_id": 1
        }
        assert self.movie_service.update(movie_d)

    def test_delete(self):
        assert self.movie_service.delete(1) is None
