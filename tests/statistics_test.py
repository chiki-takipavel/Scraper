import unittest
from movies_statistics import MoviesStatistics
from utils.constants import Constants
from datetime import date


class TestStatistics(unittest.TestCase):
    def setUp(self):
        self.stats = MoviesStatistics(None)

    def test_get_season(self):
        self.assertEqual(self.stats.get_season(date(2023, 1, 1)), Constants.WINTER)
        self.assertEqual(self.stats.get_season(date(2023, 4, 1)), Constants.SPRING)
        self.assertEqual(self.stats.get_season(date(2023, 7, 1)), Constants.SUMMER)
        self.assertEqual(self.stats.get_season(date(2023, 11, 1)), Constants.AUTUMN)

    def test_get_rate_group(self):
        self.assertEqual(self.stats.get_rate_group(0), Constants.RATE_GROUP_0_2)
        self.assertEqual(self.stats.get_rate_group(1.5), Constants.RATE_GROUP_0_2)
        self.assertEqual(self.stats.get_rate_group(2), Constants.RATE_GROUP_0_2)
        self.assertEqual(self.stats.get_rate_group(3.2), Constants.RATE_GROUP_2_4)
        self.assertEqual(self.stats.get_rate_group(4), Constants.RATE_GROUP_2_4)
        self.assertEqual(self.stats.get_rate_group(5.7), Constants.RATE_GROUP_4_6)
        self.assertEqual(self.stats.get_rate_group(6), Constants.RATE_GROUP_4_6)
        self.assertEqual(self.stats.get_rate_group(7.5), Constants.RATE_GROUP_6_8)
        self.assertEqual(self.stats.get_rate_group(8), Constants.RATE_GROUP_6_8)
        self.assertEqual(self.stats.get_rate_group(9.2), Constants.RATE_GROUP_8_10)
        self.assertEqual(self.stats.get_rate_group(10), Constants.RATE_GROUP_8_10)

    def test_count_movies_by_season(self):
        movies = [
            {"premiere_date": "2023-01-01"},
            {"premiere_date": "2023-04-01"},
            {"premiere_date": "2023-07-01"},
            {"premiere_date": "2023-11-01"},
            {"premiere_date": None},
        ]
        expected_counts = {Constants.WINTER: 1, Constants.SPRING: 1, Constants.SUMMER: 1, Constants.AUTUMN: 1}

        result = self.stats.count_movies_by_season(movies)

        self.assertEqual(result, expected_counts)

    def test_count_movies_by_country(self):
        movies = [
            {"countries": ["США"]},
            {"countries": ["США", "Франция"]},
            {"countries": ["Франция"]},
            {"countries": ["Германия", "Франция", "США"]},
            {"countries": ["Россия"]},
        ]
        expected_counts = {"США": 3, "Франция": 3, "Германия": 1, "Россия": 1}

        result = self.stats.count_movies_by_country(movies)

        self.assertEqual(result, expected_counts)

    def test_count_movies_by_genre(self):
        movies = [
            {"genres": ["Драмы"]},
            {"genres": ["Драмы", "Боевики", "Зарубежные"]},
            {"genres": ["Комедии"]},
            {"genres": ["Драмы", "Русские"]},
            {"genres": ["Триллеры"]},
        ]
        expected_counts = {"Драмы": 3, "Боевики": 1, "Комедии": 1, "Триллеры": 1}

        result = self.stats.count_movies_by_genre(movies)

        self.assertEqual(result, expected_counts)


if __name__ == '__main__':
    unittest.main()
