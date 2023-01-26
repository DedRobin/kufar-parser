import requests
import csv
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

        names, prices, links, images, dates = [], [], [], [], []

        for p in products:
            name = p.find_element(By.CLASS_NAME, "styles_title__XS_QS")
            name = name.text
            names.append(name)

            price = p.find_element(By.XPATH,
                                   '//*[@id="main-content"]/div[6]/div[1]/div/div[2]/div[2]/div/div/section[1]/a/div[2]/div[1]/div[1]/p/span[1]')
            price = price.text
            prices.append(price)

            link = p.get_attribute("href")
            links.append(link)

            image = p.find_element(By.CLASS_NAME, "styles_image__CTXvl")
            src = image.get_attribute("data-src")
            images.append(src)

            date = p.find_element(By.CLASS_NAME, 'styles_secondary__dylmH')
            date = date.find_element(By.TAG_NAME, "span")
            date = date.text
            dates.append(date)

        with open("data.csv", "w") as f:
            writer = csv.writer(f)
            data = list(zip(names, prices, links, images, dates))
            # for row in data:
            writer.writerows(data)
            # f.write("\n".join(",".join(row) for row in data))

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_html(url="https://www.kufar.by/l/r~minsk/noutbuki/nb~apple?cmp=0&cnd=1&sort=lst.d")


if __name__ == "__main__":
    main()
