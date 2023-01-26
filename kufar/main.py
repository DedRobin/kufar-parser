import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver.common.by import By


def get_html(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(url=url)
        # time.sleep(3)

        css_selector_1 = "#__next > div.styles_wrapper__YA4CR > div > div.styles_buttons__H6b2h > button"
        button = driver.find_element(By.CSS_SELECTOR, css_selector_1)
        button.click()

        class_name = "styles_wrapper__IMYdY"
        products = driver.find_elements(By.CLASS_NAME, class_name)

        links = []
        images = []
        for p in products:
            link = p.get_attribute("href")
            links.append(link)

            image = p.find_element(By.CLASS_NAME, "styles_image__CTXvl")
            src = image.get_attribute("data-src")
            images.append(src)

        time.sleep(10)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_html(url="https://www.kufar.by/l/r~minsk/noutbuki/nb~apple?cmp=0&cnd=1&sort=lst.d")


if __name__ == "__main__":
    main()
