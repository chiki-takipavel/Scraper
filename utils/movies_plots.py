import matplotlib.pyplot as plt
from utils.constants import Constants


class Plots:
    @staticmethod
    def plot_movies_by_season(seasons_counts):
        seasons = list(seasons_counts.keys())
        counts = list(seasons_counts.values())

        title = "Number of Movies by Season"
        plt.figure(figsize=(Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT), dpi=Constants.PLOT_DPI)
        plt.title(title)
        plt.xlabel("Season")
        plt.ylabel("Number of Movies")
        plt.bar(seasons, counts)
        plt.savefig(f"{Constants.PLOTS_FOLDER}/{title}.{Constants.PLOT_FILE_FORMAT}")
        plt.show()

    @staticmethod
    def plot_pie_chart(title, labels, values):
        plt.figure(figsize=(Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT), dpi=Constants.PLOT_DPI)
        plt.title(title)
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.savefig(f"{Constants.PLOTS_FOLDER}/{title}.{Constants.PLOT_FILE_FORMAT}")
        plt.show()

    def plot_movies_by_country(self, countries_counts):
        countries = list(countries_counts.keys())
        counts = list(countries_counts.values())
        title = f"Top {len(countries)} Movie Producing Countries"
        self.plot_pie_chart(title, countries, counts)

    def plot_movies_by_genre(self, genres_counts):
        genres = list(genres_counts.keys())
        counts = list(genres_counts.values())
        title = f"Top {len(genres)} Movie Genres"
        self.plot_pie_chart(title, genres, counts)

    @staticmethod
    def plot_correlation_imdb_kinopoisk(both_ratings):
        imdb_ratings, kinopoisk_ratings = both_ratings

        title = "Correlation Between IMDb and Kinopoisk Ratings"
        plt.figure(figsize=(Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT), dpi=Constants.PLOT_DPI)
        plt.title(title)
        plt.xlabel("IMDb Ratings")
        plt.ylabel("Kinopoisk Ratings")
        plt.scatter(imdb_ratings, kinopoisk_ratings, s=Constants.SCATTER_POINT_SIZE)
        frame = plt.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])
        plt.savefig(f"{Constants.PLOTS_FOLDER}/{title}.{Constants.PLOT_FILE_FORMAT}")
        plt.show()

    @staticmethod
    def plot_movies_by_rating(ratings_counts, platform="imdb"):
        if platform not in {"imdb", "kinopoisk"}:
            raise ValueError("Invalid rating type specified. Use 'imdb' or 'kinopoisk'.")

        if platform == "imdb":
            platform_name = "IMDb"
        else:
            platform_name = "Kinopoisk"

        ratings = list(ratings_counts.keys())
        counts = list(ratings_counts.values())

        title = f"Number of Movies by Rating ({platform_name})"
        plt.figure(figsize=(Constants.PLOT_WIDTH, Constants.PLOT_HEIGHT), dpi=Constants.PLOT_DPI)
        plt.title(title)
        plt.xlabel("Rate Group")
        plt.ylabel("Number of Movies")
        plt.bar(ratings, counts)
        plt.savefig(f"{Constants.PLOTS_FOLDER}/{title}.{Constants.PLOT_FILE_FORMAT}")
        plt.show()
