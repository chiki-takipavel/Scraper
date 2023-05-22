import redis
from utils.logger import Logger
from utils.movies_utils import MoviesUtils
from utils.constants import Constants
from utils.movies_plots import Plots
from datetime import datetime
import matplotlib
from collections import defaultdict


class MoviesStatistics:
    def __init__(self, logger):
        matplotlib.use("Agg")
        self.logger = logger
        self.plots = Plots()
        self.db = redis.Redis(
            host=Constants.REDIS_HOST,
            port=Constants.REDIS_PORT,
            db=Constants.REDIS_DB,
            charset=Constants.REDIS_CHARSET,
            decode_responses=True
        )
        self.utils = MoviesUtils()

    @staticmethod
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

    @staticmethod
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

    def count_movies_by_season(self, movies):
        seasons_counts = {Constants.WINTER: 0, Constants.SPRING: 0, Constants.SUMMER: 0, Constants.AUTUMN: 0}
        for movie in movies:
            premiere_date = movie["premiere_date"]
            if premiere_date:
                try:
                    date_object = datetime.fromisoformat(premiere_date).date()
                    season = self.get_season(date_object)
                    seasons_counts[season] += 1
                except ValueError as e:
                    self.logger.error(f"{premiere_date}: {e}")

        return seasons_counts

    @staticmethod
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

    @staticmethod
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

    def count_movies_by_rating(self, movies, platform="imdb"):
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
                rate_group = self.get_rate_group(rating)
                ratings_counts[rate_group] += 1

        return ratings_counts

    @staticmethod
    def count_movies_by_genre(movies, top_count=5):
        genres_counts = defaultdict(int)
        for movie in movies:
            for genre in movie["genres"]:
                if genre not in Constants.IGNORED_GENRES:
                    genres_counts[genre] += 1

        genres_count = len(genres_counts)
        if genres_count < top_count:
            top_count = genres_count

        top_genres = sorted(genres_counts.items(), key=lambda x: x[1], reverse=True)[:top_count]
        top_genres_counts = dict(top_genres)

        return top_genres_counts

    def run(self):
        movies = self.utils.get_movies_from_db(self.db)
        unique_movies = self.utils.get_unique_movies(movies)
        self.logger.debug(len(unique_movies))

        seasons_counts = self.count_movies_by_season(unique_movies)
        countries_counts = self.count_movies_by_country(unique_movies)
        genres_counts = self.count_movies_by_genre(unique_movies)
        both_ratings = self.get_both_ratings(unique_movies)
        imdb_ratings = self.count_movies_by_rating(unique_movies, "imdb")
        kinopoisk_ratings = self.count_movies_by_rating(unique_movies, "kinopoisk")

        self.plots.plot_movies_by_season(seasons_counts)
        self.plots.plot_movies_by_country(countries_counts)
        self.plots.plot_movies_by_genre(genres_counts)
        self.plots.plot_correlation_imdb_kinopoisk(both_ratings)
        self.plots.plot_movies_by_rating(imdb_ratings, "imdb")
        self.plots.plot_movies_by_rating(kinopoisk_ratings, "kinopoisk")


if __name__ == "__main__":
    MoviesStatistics(Logger.get_logger("statistics")).run()
