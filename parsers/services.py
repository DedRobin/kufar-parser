import re
from datetime import datetime, timedelta

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from settings import DAYS_AGO, LIMIT_OF_RECORDS

MONTHS = {
    "янв.": 1,
    "февр.": 2,
    "март.": 3,
    "апр.": 4,
    "мая": 5,
    "июн.": 6,
    "июл.": 7,
    "авг.": 8,
    "сент.": 9,
    "окт.": 10,
    "нояб.": 11,
    "дек.": 12,
}


def get_page(driver: WebDriver):
    products_from_page = driver.find_elements(By.TAG_NAME, "section")
    return products_from_page


def get_product_name(product: WebElement) -> str:
    name = product.find_element(By.TAG_NAME, "h3")
    name = name.text
    return name


def get_product_price(product: WebElement) -> str:
    # price = product.find_element(By.TAG_NAME, "styles_price__")
    price = product.find_elements(By.TAG_NAME, "span")[0]
    price = price.text
    return price


def get_product_link(product: WebElement) -> str:
    link = product.find_element(By.TAG_NAME, "a")
    link = link.get_attribute("href")
    return link


def get_product_image(product: WebElement) -> str:
    try:
        image = product.find_element(By.TAG_NAME, "img")
        src = image.get_attribute("data-src") or image.get_attribute("src")
        if not src:
            src = "static/images/no-image.jpg"
    except NoSuchElementException:
        src = "static/images/no-image.jpg"
    return src


def get_post_date(product: WebElement) -> str:
    # date = product.find_element(By.CLASS_NAME, "styles_secondary__dylmH")
    # date = product.find_element(By.CLASS_NAME, "styles_secondary__")
    date = product.find_elements(By.TAG_NAME, "span")[2]
    date = date.text
    date = _convert_datetime(date)
    return date


def _convert_datetime(input_datetime: str) -> str or None:
    datetime_now = datetime.now()
    date, time = input_datetime.split(",")

    if date == "Сегодня":
        date = datetime_now.strftime("%d.%m.%Y")
    elif date == "Вчера":
        if DAYS_AGO < 2:
            return None
        different = datetime_now - timedelta(days=1)
        date = different.strftime("%d.%m.%Y")
    else:
        day_str, month_str = date.split()
        month_int = MONTHS[month_str]
        current_datetime = datetime(
            year=datetime_now.year, month=month_int, day=int(day_str)
        )
        different = datetime_now - current_datetime
        if different.days >= DAYS_AGO:
            return None
        date = current_datetime.strftime("%d.%m.%Y")
    date = ", ".join([date, time])
    return date


def get_cache() -> list:
    try:
        open("cache.txt", "r")
    except FileNotFoundError:
        cache = open("cache.txt", "w")
        cache.close()
    cache = open("cache.txt", "r").read()
    if not cache:
        return []
    data = cache.split("\n")
    return data


def check_in_cache(cache: list, product_id: str) -> bool:
    if product_id not in cache:
        return False
    return True


def get_product_id(link: str) -> str:
    match = re.findall(r"/[0-9]+\?", link)
    if match:
        link = match[0][1:-1]
        return link


def save_cache(cache: list) -> None:
    size = len(cache)
    if size > LIMIT_OF_RECORDS:
        from_index = size - LIMIT_OF_RECORDS
        cache = cache[from_index:]
    with open("cache.txt", "w") as file:
        file.write("\n".join(cache))
