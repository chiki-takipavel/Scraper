import unittest
from bs4 import BeautifulSoup
from scraper import Scraper


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper(None)
        html = """
            <html>
                <body>
                    <div class="b-post__title"> 
                        <h1 itemprop="name">Тестовый фильм</h1>
                    </div>
                    <div class="b-post__origtitle" itemprop="alternativeHeadline">Тестовый фильм / Test movie</div>
                    <table class="b-post__info">
                        <tbody>
                            <tr>
                                <td>
                                    <span class="b-post__info_rates imdb">
                                        <span class="bold">8.2</span>
                                    </span>
                                    <span class="b-post__info_rates kp">
                                        <span class="bold">7.71</span>
                                    </span>
                                </td>
                            <tr>
                                <td>8 сентября <a href="https://hdrezka.co/year/2013/">2013 года</a></td>
                            </tr>
                            <tr>
                                <td>
                                    <a href="https://hdrezka.co/country/USA/">США</a>, 
                                    <a href="https://hdrezka.co/country/UK/">Великобритания</a>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <a href="https://hdrezka.co/films/drama/"><span itemprop="genre">Драмы</span></a>, 
                                    <a href="https://hdrezka.co/films/thriller/"><span itemprop="genre">Триллеры</span></a>
                                </td>
                            </tr>
                            <tr>
                                <td itemprop="duration">120 мин.</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="b-post__description_text">Описание тестового фильма.</div>
                </body>
            </html>
            """

        self.soup = BeautifulSoup(html, "html.parser")

    def test_get_title(self):
        result = self.scraper.get_title(self.soup)

        self.assertEqual(result, "Тестовый фильм")

    def test_get_original_title(self):
        result = self.scraper.get_original_title(self.soup)

        self.assertEqual(result, "Тестовый фильм / Test movie")

    def test_get_description(self):
        result = self.scraper.get_description(self.soup)

        self.assertEqual(result, "Описание тестового фильма.")

    def test_get_genres(self):
        result = self.scraper.get_genres(self.soup)

        self.assertEqual(result, ["Драмы", "Триллеры"])

    def test_get_duration(self):
        result = self.scraper.get_duration(self.soup)

        self.assertEqual(result, "120 мин.")

    def test_get_countries(self):
        result = self.scraper.get_countries(self.soup)

        self.assertEqual(result, ["США", "Великобритания"])

    def test_get_premier_date(self):
        result = self.scraper.get_premier_date(self.soup)

        self.assertEqual(result, ("2013-09-08", "2013"))

    def test_get_imdb_rate(self):
        result = self.scraper.get_imdb_rate(self.soup)

        self.assertEqual(result, "8.2")

    def test_get_kinopoisk_rate(self):
        result = self.scraper.get_kinopoisk_rate(self.soup)

        self.assertEqual(result, "7.71")
