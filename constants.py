class Constants:
    BASE_URL = "https://www.hdrezka.co"

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    HTML_PARSER = "html.parser"

    H1_TAG = "h1"
    TD_TAG = "td"
    LINK_TAG = "a"
    DIV_TAG = "div"
    SPAN_TAG = "span"
    PARAGRAPH_TAG = "p"

    HREF_ATTRIBUTE = "href"

    FILMS_ITEM_CLASS = "b-content__inline_items"
    FILM_LINK_CLASS = "b-content__inline_item-link"
    TITLE_ITEMPROP = "name"
    TITLE_ORIGINAL_ITEMPROP = "alternativeHeadline"
    DESCRIPTION_CLASS = "b-post__description_text"
    GENRE_ITEMPROP = "genre"
    DURATION_ITEMPROP = "duration"
    COUNTRY = r"/country/"
    YEAR = r"/year/(\d+)/"
    PREMIERE_DATE = r"(?P<full_date>(?P<day>\d{1,2}) (?P<month>\w+) (?P<year>\d{4})) года"
    IMDB_CLASS = "b-post__info_rates imdb"
    KINOPOISK_CLASS = "b-post__info_rates kp"

    DATE_FORMAT = "%d %B %Y"

    RUSSIAN_MONTHS = {
        "января": "January",
        "февраля": "February",
        "марта": "March",
        "апреля": "April",
        "мая": "May",
        "июня": "June",
        "июля": "July",
        "августа": "August",
        "сентября": "September",
        "октября": "October",
        "ноября": "November",
        "декабря": "December"
    }
