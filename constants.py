class Constants:
    BASE_URL = "https://hdrezka.co"

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_CHARSET = "utf-8"

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38"
    ]
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
    PREMIERE_DATE = r"^(?P<full_date>((?P<day>\d{1,2})\s+(?P<month>\w{3,8})\s+)?(?P<year>\d{4}))(\s+года)?$"
    IMDB_CLASS = "b-post__info_rates imdb"
    KINOPOISK_CLASS = "b-post__info_rates kp"

    HDREZKA_DATE_FORMAT = "%d %B %Y"
    ISO_DATE_FORMAT = "%Y-%m-%d"
    EMPTY_STRING = ""

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

    WINTER = "Winter"
    SPRING = "Spring"
    SUMMER = "Summer"
    AUTUMN = "Autumn"