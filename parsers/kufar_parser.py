import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from parsers.tools import get_product_name, get_product_price, get_product_link, get_product_image, get_post_date, \
    get_page, check_in_cache, get_cache

URL = "https://www.kufar.by/l/r~minsk/noutbuki/nb~apple?cmp=0&cnd=1&sort=lst.d"


def parse_kufar(url: str = URL) -> list:
    products = []

    # Options
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--window-size=1920,1080')

    # Open browser
    driver = webdriver.Chrome(executable_path="driver/chromedriver", options=options)
    driver.get(url=url)

    # Click button "Принять"
    # driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/button').click()

    # Signal
    run_loop = True

    # Cache
    # try:
    #     cache = open("cache.csv", "r")
    # except FileNotFoundError:
    cache = get_cache()

    # Run loop
    while run_loop:

        products_from_page = get_page(driver)

        names, prices, links, images, dates = [], [], [], [], []

        for num, product in enumerate(products_from_page, 1):
            date = get_post_date(product)
            if not date:
                run_loop = False
                break

            link = get_product_link(product)
            is_existed = check_in_cache(cache, link)  # Checking a file in the cache
            if is_existed:
                continue

            name = get_product_name(product)

            price = get_product_price(product)

            src_image = get_product_image(product)

            dates.append(date)
            links.append(link)
            names.append(name)
            prices.append(price)
            images.append(src_image)

        product_list = list(zip(links, names, prices, dates, images))
        products.append(product_list)

        # Get next page
        next_page = driver.find_elements(By.CLASS_NAME, 'styles_link__KajLs.styles_arrow__fJMcy')
        last_element = next_page[-1]
        if last_element.tag_name != "a":
            run_loop = False
        else:
            next_url = last_element.get_attribute("href")
            driver.get(url=next_url)

    # Closing cachefile and browser
    cache.close()
    driver.close()
    driver.quit()
    return products
