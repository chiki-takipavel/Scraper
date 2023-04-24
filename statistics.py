import redis
from utils.logger import get_logger
from utils.movies_utils import get_movies_from_db, get_unique_movies
from utils.constants import Constants
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict


logger = get_logger("statistics")


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


def get_rate_group(rating):
    rating = float(rating)
    if 0 <= rating <= 2:
        return Constants.RATE_GROUP_0_2
    elif 2 < rating <= 4:
        return Constants.RATE_GROUP_2_4
    elif 4 < rating <= 6:
        return Constants.RATE_GROUP_4_6
    elif 6 < rating <= 8:
        return Constants.RATE_GROUP_6_8
    else:
        return Constants.RATE_GROUP_8_10


def count_movies_by_season(movies):
    seasons_counts = {Constants.WINTER: 0, Constants.SPRING: 0, Constants.SUMMER: 0, Constants.AUTUMN: 0}
    for movie in movies:
        premiere_date = movie["premiere_date"]
        if premiere_date:
            try:
                date_object = datetime.fromisoformat(premiere_date).date()
                season = get_season(date_object)
                seasons_counts[season] += 1
            except ValueError as e:
                logger.error(f"{premiere_date}: {e}")

    return seasons_counts


def count_movies_by_country(movies, top_count=5):
    countries_counts = defaultdict(int)
    for movie in movies:
        for country in movie["countries"]:
            countries_counts[country] += 1

    countries_count = len(countries_counts)
    if countries_count < top_count:
        top_count = countries_count

    top_countries = sorted(countries_counts.items(), key=lambda x: x[1], reverse=True)[:top_count]
    top_countries_counts = dict(top_countries)

    return top_countries_counts


def get_both_ratings(movies):
    imdb_ratings = []
    kinopoisk_ratings = []
    for movie in movies:
        rate_imdb = movie["rate_imdb"]
        rate_kinopoisk = movie["rate_kinopoisk"]
        if rate_imdb and rate_kinopoisk:
            imdb_ratings.append(rate_imdb)
            kinopoisk_ratings.append(rate_kinopoisk)

    return imdb_ratings, kinopoisk_ratings


def count_movies_by_rating(movies, platform="imdb"):
    if platform not in {"imdb", "kinopoisk"}:
        raise ValueError("Invalid rating type specified. Use 'imdb' or 'kinopoisk'.")

    ratings_counts = {
        Constants.RATE_GROUP_0_2: 0,
        Constants.RATE_GROUP_2_4: 0,
        Constants.RATE_GROUP_4_6: 0,
        Constants.RATE_GROUP_6_8: 0,
        Constants.RATE_GROUP_8_10: 0
    }
    for movie in movies:
        if platform == "imdb":
            rating = movie["rate_imdb"]
        else:
            rating = movie["rate_kinopoisk"]

        if rating:
            rate_group = get_rate_group(rating)
            ratings_counts[rate_group] += 1

    return ratings_counts


def count_movies_by_genre(movies, top_count=5):
    genres_counts = defaultdict(int)
    for movie in movies:
        for genre in movie["genres"]:
            genres_counts[genre] += 1

    genres_count = len(genres_counts)
    if genres_count < top_count:
        top_count = genres_count

    top_genres = sorted(genres_counts.items(), key=lambda x: x[1], reverse=True)[:top_count]
    top_genres_counts = dict(top_genres)

    return top_genres_counts


def plot_movies_by_season(seasons_counts):
    seasons = list(seasons_counts.keys())
    counts = list(seasons_counts.values())

    plt.figure(figsize=(Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT), dpi=Constants.PLOT_DPI)
    plt.title("Number of Movies by Season")
    plt.xlabel("Season")
    plt.ylabel("Number of Movies")
    plt.bar(seasons, counts)
    plt.show()


def plot_pie_chart(title, labels, values):
    plt.figure(figsize=(Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT), dpi=Constants.PLOT_DPI)
    plt.title(title)
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.show()


def plot_movies_by_country(countries_counts):
    countries = list(countries_counts.keys())
    counts = list(countries_counts.values())
    title = f"Top {len(countries)} Movie Producing Countries"
    plot_pie_chart(title, countries, counts)


def plot_movies_by_genre(genres_counts):
    genres = list(genres_counts.keys())
    counts = list(genres_counts.values())
    title = f"Top {len(genres)} Movie Genres"
    plot_pie_chart(title, genres, counts)


def plot_correlation_imdb_kinopoisk(both_ratings):
    imdb_ratings, kinopoisk_ratings = both_ratings

    plt.figure(figsize=(Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT), dpi=Constants.PLOT_DPI)
    plt.title("Correlation Between IMDb and Kinopoisk Ratings")
    plt.xlabel("IMDb Ratings")
    plt.ylabel("Kinopoisk Ratings")
    plt.scatter(imdb_ratings, kinopoisk_ratings)
    frame = plt.gca()
    frame.axes.get_xaxis().set_ticks([])
    frame.axes.get_yaxis().set_ticks([])
    plt.show()


def plot_movies_by_rating(ratings_counts, platform="imdb"):
    if platform not in {"imdb", "kinopoisk"}:
        raise ValueError("Invalid rating type specified. Use 'imdb' or 'kinopoisk'.")

    if platform == "imdb":
        platform_name = "IMDb"
    else:
        platform_name = "Kinopoisk"

    ratings = list(ratings_counts.keys())
    counts = list(ratings_counts.values())

    plt.figure(figsize=(Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT), dpi=Constants.PLOT_DPI)
    plt.title(f"Number of Movies by Rating ({platform_name})")
    plt.xlabel("Rate Group")
    plt.ylabel("Number of Movies")
    plt.bar(ratings, counts)
    plt.show()


def main():
    with redis.Redis(
        host=Constants.REDIS_HOST,
        port=Constants.REDIS_PORT,
        db=Constants.REDIS_DB,
        charset=Constants.REDIS_CHARSET,
        decode_responses=True
    ) as db:
        movies = get_movies_from_db(db)

    unique_movies = get_unique_movies(movies)

    seasons_counts = count_movies_by_season(unique_movies)
    countries_counts = count_movies_by_country(unique_movies)
    genres_counts = count_movies_by_genre(unique_movies)
    both_ratings = get_both_ratings(unique_movies)
    imdb_ratings = count_movies_by_rating(unique_movies, "imdb")
    kinopoisk_ratings = count_movies_by_rating(unique_movies, "kinopoisk")

    plot_movies_by_season(seasons_counts)
    plot_movies_by_country(countries_counts)
    plot_movies_by_genre(genres_counts)
    plot_correlation_imdb_kinopoisk(both_ratings)
    plot_movies_by_rating(imdb_ratings, "imdb")
    plot_movies_by_rating(kinopoisk_ratings, "kinopoisk")


if __name__ == "__main__":
    main()
