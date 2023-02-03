from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

URL = "https://www.kufar.by/l/r~minsk/noutbuki/nb~apple?cmp=0&cnd=1&sort=lst.d"


def parse_kufar(url: str = URL) -> list:
    products = []

    # Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--window-size=1920,1080')

    # Open browser
    driver = webdriver.Chrome(executable_path="driver/chromedriver", options=chrome_options)
    driver.get(url=url)

    # Click button "Принять"
    # driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/button').click()

    # Signal
    signal = True

    while signal:
        products_from_page = driver.find_elements(By.TAG_NAME, "section")  # [:5]

        names, prices, links, images, dates = [], [], [], [], []

        for num, p in enumerate(products_from_page, 1):
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

        product_list = list(zip(links, names, prices, dates, images))
        products.append(product_list)

        # Get next page
        next_page = driver.find_elements(By.CLASS_NAME, 'styles_link__KajLs.styles_arrow__fJMcy')

        last_element = next_page[-1]
        if last_element.tag_name != "a":
            break
        next_url = last_element.get_attribute("href")
        try:
            driver.get(url=next_url)
        except Exception as _ex:
            print(_ex)

    # Closing browser
    driver.close()
    driver.quit()
    return products
