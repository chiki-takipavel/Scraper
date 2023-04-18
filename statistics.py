import json
import redis
from constants import Constants
from datetime import datetime
import matplotlib.pyplot as plt


def get_movies_from_db(connection):
    movie_keys = connection.keys("movie:*")
    movies = [json.loads(connection.get(key)) for key in movie_keys]

    return movies


def get_unique_movies(movies):
    unique_movies = []
    seen_movies = set()

    for movie in movies:
        title_year = (movie["title"], movie["year"])

        if title_year not in seen_movies:
            unique_movies.append(movie)
            seen_movies.add(title_year)

    return unique_movies


def get_season(date):
    month = date.month
    if 3 <= month <= 5:
        return Constants.SPRING
    elif 6 <= month <= 8:
        return Constants.SUMMER
    elif 9 <= month <= 11:
        return Constants.AUTUMN
    else:
        return Constants.WINTER


def count_movies_by_season(movies):
    season_counts = {Constants.WINTER: 0, Constants.SPRING: 0, Constants.SUMMER: 0, Constants.AUTUMN: 0}

    for movie in movies:
        premiere_date = movie["premiere_date"]
        if premiere_date:
            try:
                date_object = datetime.fromisoformat(premiere_date).date()
                season = get_season(date_object)
                season_counts[season] += 1
            except ValueError as e:
                print(f"Error: {premiere_date}: {e}")

    return season_counts


def plot_movies_by_season(season_counts):
    seasons = list(season_counts.keys())
    counts = list(season_counts.values())

    plt.bar(seasons, counts)
    plt.xlabel("Season")
    plt.ylabel("Number of Movies")
    plt.title("Number of Movies by Season")
    plt.show()


def main():
    db = redis.Redis(
        host=Constants.REDIS_HOST,
        port=Constants.REDIS_PORT,
        db=Constants.REDIS_DB,
        charset=Constants.REDIS_CHARSET,
        decode_responses=True
    )

    movies = get_movies_from_db(db)
    unique_movies = get_unique_movies(movies)
    season_counts = count_movies_by_season(unique_movies)
    plot_movies_by_season(season_counts)


if __name__ == "__main__":
    main()
