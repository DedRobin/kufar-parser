from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from parsers.services import (
    check_in_cache,
    get_cache,
    get_page,
    get_post_date,
    get_product_id,
    get_product_image,
    get_product_link,
    get_product_name,
    get_product_price,
    save_cache,
)


def parse_kufar(url: str) -> list:
    products = []

    # Options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    # Open browser
    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url=url)

    # Click button "Принять"
    # driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/button').click()

    # Signal
    run_loop = True

    cache = get_cache()

    # Run loop
    while run_loop:
        products_from_page = get_page(driver)

        names, prices, links, images, dates = [], [], [], [], []

        for product in products_from_page:
            try:
                product.find_element(By.TAG_NAME, "object")
            except NoSuchElementException:
                date = get_post_date(product)
                if not date:
                    product_list = list(zip(links, names, prices, dates, images))
                    if product_list:
                        products.append(product_list)
                    # Closing the browser
                    driver.close()
                    driver.quit()
                    save_cache(cache)
                    return products

                link = get_product_link(product)
                product_id = get_product_id(link)
                is_existed = check_in_cache(
                    cache, product_id
                )  # Checking a file in the cache
                if is_existed:
                    continue
                else:
                    cache.append(product_id)
                name = get_product_name(product)
                price = get_product_price(product)
                src_image = get_product_image(product)

                dates.append(date)
                links.append(link)
                names.append(name)
                prices.append(price)
                images.append(src_image)
            else:
                continue

        product_list = list(zip(links, names, prices, dates, images))
        if product_list:
            products.append(product_list)

        # Get next page
        next_page = driver.find_elements(
            By.CLASS_NAME, "styles_link__KajLs.styles_arrow__fJMcy"
        )
        last_child = next_page[-1]
        if last_child.tag_name != "a":
            run_loop = False
        else:
            next_url = last_child.get_attribute("href")
            driver.get(url=next_url)

    # Closing the browser
    driver.close()
    driver.quit()
    save_cache(cache)
    return products
