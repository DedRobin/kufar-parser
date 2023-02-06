from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_page(driver):
    products_from_page = driver.find_elements(By.TAG_NAME, "section")[:5]
    return products_from_page


def get_product_name(product):
    name = product.find_element(By.CLASS_NAME, "styles_title__XS_QS")
    name = name.text
    return name


def get_product_price(product):
    price = product.find_element(By.CLASS_NAME, 'styles_price__tiO8k')
    price = price.find_element(By.TAG_NAME, "span")
    price = price.text
    return price


def get_product_link(product):
    link = product.find_element(By.CLASS_NAME, 'styles_wrapper__IMYdY')
    link = link.get_attribute("href")
    return link


def get_product_image(product):
    try:
        image = product.find_element(By.CLASS_NAME, "styles_image__CTXvl")
        src = image.get_attribute("data-src")
    except NoSuchElementException:
        src = "static/images/no-image.jpg"
    return src


def get_post_date(product):
    date = product.find_element(By.CLASS_NAME, 'styles_secondary__dylmH')
    date = date.find_element(By.TAG_NAME, "span")
    date = date.text
    date = _convert_datetime(date)
    return date


def _convert_datetime(input_datetime):
    datetime_now = datetime.now()
    input_datetime = input_datetime.split(",")

    if input_datetime[0] == "Сегодня":
        input_datetime[0] = datetime_now.strftime('%d.%m.%Y')
    elif input_datetime[0] == "Вчера":
        different = datetime_now - timedelta(days=1)
        input_datetime[0] = different.strftime('%d.%m.%Y')

    convert_datetime = ", ".join(input_datetime)
    return convert_datetime
