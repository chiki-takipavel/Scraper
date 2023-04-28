import json
from collections import defaultdict


def get_movies_from_db(connection):
    movie_keys = connection.scan_iter("movie:*")
    movies = [json.loads(connection.get(key)) for key in movie_keys]

    return movies


def get_unique_movies(movies):
    unique_movies = []
    seen_movies = set()
    for movie in movies:
        title_year = (movie["title_original"], movie["year"])
        if title_year not in seen_movies:
            unique_movies.append(movie)
            seen_movies.add(title_year)

    return unique_movies


def get_genres_classes(movies):
    movies_genres = defaultdict(int)
    for movie in movies:
        genres = movie["genres"]
        if genres:
            first_genre = genres[0]
            if first_genre:
                movies_genres[first_genre] += 1

    genres = dict(sorted(movies_genres.items(), key=lambda x: x[1], reverse=True)[:5])
    genres_classes = list(genres.keys())

    return genres_classes
