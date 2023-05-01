class Constants:
    BASE_URL = "https://hdrezka.co"

    REDIS_HOST = "redis"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_CHARSET = "utf-8"

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.43",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
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

    IGNORED_GENRES = ["Зарубежные", "Русские", "Советские", "Украинские"]

    RATE_GROUP_0_2 = "[0-2]"
    RATE_GROUP_2_4 = "(2-4]"
    RATE_GROUP_4_6 = "(4-6]"
    RATE_GROUP_6_8 = "(6-8]"
    RATE_GROUP_8_10 = "(8-10]"

    PLOT_HEIGHT = 4
    PLOT_WIDTH = 6
    PLOT_DPI = 600
    SCATTER_POINT_SIZE = 2

    PLOTS_FOLDER = "./plots"
    PLOT_FILE_FORMAT = "png"
