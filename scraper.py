import json
import requests
import re
from bs4 import BeautifulSoup
import random
import redis
from time import sleep
from utils.constants import Constants
from utils.logger import Logger
from datetime import datetime


class Scraper:
    def __init__(self, logger):
        self.logger = logger
        self.session = requests.Session()
        self.db = redis.Redis(
            host=Constants.REDIS_HOST,
            port=Constants.REDIS_PORT,
            db=Constants.REDIS_DB,
            charset=Constants.REDIS_CHARSET,
            decode_responses=True
        )

    @staticmethod
    def get_random_user_agent():
        return random.choice(Constants.USER_AGENTS)

    def get_soup(self, url, max_retries=5):
        retry_count = 0
        while retry_count < max_retries:
            user_agent = self.get_random_user_agent()
            self.session.headers.update({"User-Agent": user_agent})
            response = self.session.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text, Constants.HTML_PARSER)
            else:
                self.logger.warning(f"Status code: {response.status_code}")

                Constants.USER_AGENTS.remove(user_agent)
                if not Constants.USER_AGENTS:
                    return None

                retry_count += 1

        return None

    @staticmethod
    def get_movie_links(soup):
        links = []
        films = soup.find(Constants.DIV_TAG, class_=Constants.FILMS_ITEM_CLASS)
        if films:
            for movie_link in films.find_all(Constants.DIV_TAG, class_=Constants.FILM_LINK_CLASS):
                if movie_link:
                    links.append(movie_link.find(Constants.LINK_TAG)[Constants.HREF_ATTRIBUTE])

        return links

    def get_movie_details(self, url):
        soup = self.get_soup(url)
        if not soup:
            return None

        title = self.get_title(soup)
        title_original = self.get_original_title(soup)
        description = self.get_description(soup)
        genres = self.get_genres(soup)
        duration = self.get_duration(soup)
        countries = self.get_countries(soup)
        premier_date, year = self.get_premier_date(soup)
        rate_imdb = self.get_imdb_rate(soup)
        rate_kinopoisk = self.get_kinopoisk_rate(soup)

        if not title_original:
            title_original = title

        return {
            "title": title,
            "title_original": title_original,
            "description": description,
            "year": year,
            "genres": genres,
            "countries": countries,
            "duration": duration,
            "premiere_date": premier_date,
            "rate_imdb": rate_imdb,
            "rate_kinopoisk": rate_kinopoisk
        }

    @staticmethod
    def get_title(soup):
        title = ""
        title_element = soup.find(Constants.H1_TAG, itemprop=Constants.TITLE_ITEMPROP)
        if title_element:
            title = title_element.text.strip()

        return title

    @staticmethod
    def get_original_title(soup):
        title_original = ""
        title_original_element = soup.find(Constants.DIV_TAG, itemprop=Constants.TITLE_ORIGINAL_ITEMPROP)
        if title_original_element:
            title_original = title_original_element.text.strip()

        return title_original

    @staticmethod
    def get_description(soup):
        description = ""
        description_element = soup.find(Constants.DIV_TAG, class_=Constants.DESCRIPTION_CLASS)
        if description_element:
            description = description_element.text.strip()

        return description

    @staticmethod
    def get_genres(soup):
        genres = []
        for genre in soup.find_all(Constants.SPAN_TAG, itemprop=Constants.GENRE_ITEMPROP):
            genres.append(genre.text.strip())

        return genres

    @staticmethod
    def get_countries(soup):
        countries = []
        pattern = re.compile(Constants.COUNTRY)
        for country in soup.find_all(Constants.LINK_TAG, href=pattern):
            countries.append(country.text.strip())

        return countries

    @staticmethod
    def get_duration(soup):
        duration = ""
        duration_element = soup.find(Constants.TD_TAG, itemprop=Constants.DURATION_ITEMPROP)
        if duration_element:
            duration = duration_element.text.strip()

        return duration

    @staticmethod
    def get_premier_date(soup):
        pattern_year = re.compile(Constants.YEAR)
        year_element = soup.find(Constants.LINK_TAG, href=pattern_year)
        if not year_element:
            return Constants.EMPTY_STRING, Constants.EMPTY_STRING

        pattern_date = re.compile(Constants.PREMIERE_DATE)
        premier_date = year_element.parent.text.strip()
        match = pattern_date.search(premier_date)
        if not match:
            return Constants.EMPTY_STRING, Constants.EMPTY_STRING

        premier_date = match.group("full_date")
        year = match.group("year")
        if premier_date != year:
            for rus, eng in Constants.RUSSIAN_MONTHS.items():
                premier_date = premier_date.replace(rus, eng)

            parsed_date = datetime.strptime(premier_date, Constants.HDREZKA_DATE_FORMAT).date()
            premier_date = parsed_date.isoformat()

        return premier_date, year

    @staticmethod
    def get_imdb_rate(soup):
        imdb_rate = ""
        imdb_span = soup.find(Constants.SPAN_TAG, class_=Constants.IMDB_CLASS)
        if imdb_span:
            imdb_rate = imdb_span.find(Constants.SPAN_TAG).text.strip()

        return imdb_rate

    @staticmethod
    def get_kinopoisk_rate(soup):
        kp_rate = ""
        kp_span = soup.find(Constants.SPAN_TAG, class_=Constants.KINOPOISK_CLASS)
        if kp_span:
            kp_rate = kp_span.find(Constants.SPAN_TAG).text.strip()

        return kp_rate

    def scrape(self):
        page_num = 1
        while True:
            self.logger.info(f"Analyze page: {page_num}")
            url = f"{Constants.BASE_URL}/page/{page_num}/"
            soup = self.get_soup(url)
            if not soup:
                break

            movie_links = self.get_movie_links(soup)
            if not movie_links:
                break

            for link in movie_links:
                self.logger.info(f"Analyze film: {link}")
                movie_details = self.get_movie_details(link)
                if movie_details:
                    movie_key = f"movie:{movie_details['title_original']}:{movie_details['year']}"
                    movie_details_json = json.dumps(movie_details)
                    self.db.set(movie_key, movie_details_json)
                    self.logger.info(f"Added film: {movie_details['title_original']}")

                sleep(random.uniform(1, 3))

            page_num += 1
            sleep(random.uniform(2, 5))


if __name__ == "__main__":
    scraper = Scraper(Logger.get_logger("scraper"))
    scraper.scrape()
