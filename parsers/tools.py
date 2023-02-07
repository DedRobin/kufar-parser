import csv
from datetime import datetime, timedelta
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

MONTHS = {
    "янв.": 1, "февр.": 2,  # Winter
    "март.": 3, "апр.": 4, "мая": 5,  # Spring
    "июн.": 6, "июл.": 7, "аг.": 8,  # Summer
    "сент.": 9, "окт.": 10, "нояб.": 11,  # Autumn
    "дек.": 12  # Winter
}


def get_page(driver: WebDriver):
    products_from_page = driver.find_elements(By.TAG_NAME, "section")
    return products_from_page


def get_product_name(product: WebElement) -> str:
    name = product.find_element(By.CLASS_NAME, "styles_title__XS_QS")
    name = name.text
    return name


def get_product_price(product: WebElement) -> str:
    price = product.find_element(By.CLASS_NAME, 'styles_price__tiO8k')
    price = price.find_element(By.TAG_NAME, "span")
    price = price.text
    return price


def get_product_link(product: WebElement) -> str:
    link = product.find_element(By.CLASS_NAME, 'styles_wrapper__IMYdY')
    link = link.get_attribute("href")
    return link


def get_product_image(product: WebElement) -> str:
    try:
        image = product.find_element(By.CLASS_NAME, "styles_image__CTXvl")
        src = image.get_attribute("data-src")
    except NoSuchElementException:
        src = "static/images/no-image.jpg"
    return src


def get_post_date(product: WebElement) -> str:
    date = product.find_element(By.CLASS_NAME, 'styles_secondary__dylmH')
    date = date.find_element(By.TAG_NAME, "span")
    date = date.text
    date = _convert_datetime(date)
    return date


def _convert_datetime(input_datetime: str) -> str or None:
    datetime_now = datetime.now()
    date, time = input_datetime.split(",")

    if date == "Сегодня":
        date = datetime_now.strftime('%d.%m.%Y')
    elif date == "Вчера":
        different = datetime_now - timedelta(days=1)
        date = different.strftime('%d.%m.%Y')
    else:
        day_str, month_str = date.split()
        month_int = MONTHS[month_str]
        some_datetime = datetime(year=datetime_now.year, month=month_int, day=int(day_str))
        different = datetime_now - some_datetime
        if different.days > 3:
            return None
        date = some_datetime.strftime('%d.%m.%Y')
    date = ", ".join([date, time])
    return date


def get_cache() -> list:
    try:
        cache = open('cache.csv', 'r')
    except FileNotFoundError:
        cache = open('cache.csv', 'r')
        writer = csv.writer(cache)
        writer.writerow(["links"])
        cache.close()
    reader = csv.reader(cache)
    data = [row for row in reade
    return data


def check_in_cache(data_from_cache: list, link: str) -> None:
    if link in data_from_cache:
        with open("cache.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(link)
