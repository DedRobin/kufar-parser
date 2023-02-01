import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

URL = "https://www.kufar.by/l/r~minsk/noutbuki/nb~apple?cmp=0&cnd=1&sort=lst.d"


def parse_kufar(url: str = URL) -> list:
    # Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--window-size=1920,1080')

    # Open browser
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url=url)
    class_name = "styles_wrapper__IMYdY"
    products = driver.find_elements(By.TAG_NAME, "section")  # [:5]

    names, prices, links, images, dates = [], [], [], [], []

    for num, p in enumerate(products, 1):
        name = p.find_element(By.CLASS_NAME, "styles_title__XS_QS")
        name = name.text
        names.append(name)

        price = p.find_element(By.CLASS_NAME,
                               'styles_price__tiO8k')
        price = price.find_element(By.TAG_NAME, "span")
        price = price.text
        prices.append(price)

        link = p.find_element(By.CLASS_NAME, 'styles_wrapper__IMYdY')
        link = link.get_attribute("href")
        links.append(link)

        try:
            image = p.find_element(By.CLASS_NAME, "styles_image__CTXvl")
            src = image.get_attribute("data-src")
        except NoSuchElementException:
            src = "static/images/no-image.jpg"

        images.append(src)

        date = p.find_element(By.CLASS_NAME, 'styles_secondary__dylmH')
        date = date.find_element(By.TAG_NAME, "span")
        date = date.text
        dates.append(date)

    data = list(zip(links, names, prices, dates, images))

    driver.close()
    driver.quit()
    return data
