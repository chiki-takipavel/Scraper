import json


class MoviesUtils:
    @staticmethod
    def get_movies_from_db(connection):
        movie_keys = connection.scan_iter("movie:*")
        movies = [json.loads(connection.get(key)) for key in movie_keys]

        return movies

    @staticmethod
    def get_unique_movies(movies):
        unique_movies = []
        seen_movies = set()
        for movie in movies:
            title_year = (movie["title_original"], movie["year"])
            if title_year not in seen_movies:
                unique_movies.append(movie)
                seen_movies.add(title_year)

    return unique_movies
