import requests
import re
from bs4 import BeautifulSoup
import redis
from time import sleep
from constants import Constants
from datetime import datetime


def get_soup(url):
    session = requests.Session()
    headers = {
        "User-Agent": Constants.USER_AGENT
    }
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return None

    return BeautifulSoup(response.text, Constants.HTML_PARSER)


def get_movie_links(soup):
    links = []
    films = soup.find(Constants.DIV_TAG, class_=Constants.FILMS_ITEM_CLASS)
    if films:
        for movie_link in films.find_all(Constants.DIV_TAG, class_=Constants.FILM_LINK_CLASS):
            if movie_link:
                links.append(movie_link.find(Constants.LINK_TAG)[Constants.HREF_ATTRIBUTE])

    return links


def get_movie_details(url):
    soup = get_soup(url)
    if not soup:
        return None

    title = soup.find(Constants.H1_TAG, itemprop=Constants.TITLE_ITEMPROP).text.strip()
    title_original = soup.find(Constants.DIV_TAG, itemprop=Constants.TITLE_ORIGINAL_ITEMPROP).text.strip()
    description = soup.find(Constants.DIV_TAG, class_=Constants.DESCRIPTION_CLASS).text.strip()
    genres = get_genres(soup)
    duration = soup.find(Constants.TD_TAG, itemprop=Constants.DURATION_ITEMPROP).text.strip()
    countries = get_countries(soup)
    premier_date, year = get_premier_date(soup)
    rate_imdb = get_imdb_rate(soup)
    rate_kinopoisk = get_kinopoisk_rate(soup)

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


def get_genres(soup):
    genres = []
    for genre in soup.find_all(Constants.SPAN_TAG, itemprop=Constants.GENRE_ITEMPROP):
        genres.append(genre.text.strip())

    return genres


def get_countries(soup):
    countries = []
    pattern = re.compile(Constants.COUNTRY)
    for country in soup.find_all(Constants.LINK_TAG, href=pattern):
        countries.append(country.text.strip())

    return countries


def get_premier_date(soup):
    year = ""
    pattern_year = re.compile(Constants.YEAR)
    year_element = soup.find(Constants.LINK_TAG, href=pattern_year)

    pattern_date = re.compile(Constants.PREMIERE_DATE)
    premier_date = year_element.parent.text.strip()

    match = pattern_date.search(premier_date)
    if match:
        premier_date = match.group("full_date")
        year = match.group("year")

    for rus, eng in Constants.RUSSIAN_MONTHS.items():
        premier_date = premier_date.replace(rus, eng)

    parsed_date = datetime.strptime(premier_date, Constants.DATE_FORMAT).date()

    return parsed_date, year


def get_imdb_rate(soup):
    imdb_rate = ""
    imdb_span = soup.find(Constants.SPAN_TAG, class_=Constants.IMDB_CLASS)
    if imdb_span:
        imdb_rate = imdb_span.find(Constants.SPAN_TAG).text.strip()

    return imdb_rate


def get_kinopoisk_rate(soup):
    kp_rate = ""
    kp_span = soup.find(Constants.SPAN_TAG, class_=Constants.KINOPOISK_CLASS)
    if kp_span:
        kp_rate = kp_span.find(Constants.SPAN_TAG).text.strip()

    return kp_rate


def main():
    db = redis.Redis(host=Constants.REDIS_HOST, port=Constants.REDIS_PORT, db=Constants.REDIS_DB)

    page_num = 1
    while True:
        print(f"Обрабатываем страницу {page_num}")
        url = f"{Constants.BASE_URL}/page/{page_num}"
        soup = get_soup(url)
        if not soup:
            break

        movie_links = get_movie_links(soup)
        if not movie_links:
            break

        for link in movie_links:
            print(f"Обрабатываем фильм: {link}")
            movie_details = get_movie_details(link)
            if movie_details:
                movie_key = f"movie:{movie_details['title_original']}:{movie_details['year']}"
                db.hset(movie_key, mapping=movie_details)
                print(f"Добавлен фильм: {movie_details['title_original']}")

        page_num += 1
        sleep(1)


if __name__ == "__main__":
    main()
