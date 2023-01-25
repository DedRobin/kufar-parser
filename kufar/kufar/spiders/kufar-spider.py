import requests
import scrapy
import shutil
from scrapy.crawler import CrawlerProcess


class KufarSpider(scrapy.Spider):
    name = "kufar.by"
    start_urls = ["https://www.kufar.by/l/r~minsk/noutbuki/nb~apple?cmp=0&cnd=1&sort=lst.d"]

    # def start_requests(self):
    #     urls = ["https://www.kufar.by/l/r~minsk/noutbuki/nb~apple?cmp=0&cnd=1&sort=lst.d"]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        count = 0
        output = []
        for product in response.css(".styles_cards__6Mcav section"):
            image = product.css(".styles_image__HfSYp img::attr(data-src)").get()
            # image_url = response.urljoin(image)
            response = requests.get(image, stream=True)

            if response.status_code == 200:
                response.raw.decode_content = True
                with open(f"images/image-{count + 1}.png", "ab") as f:
                    shutil.copyfileobj(response.raw, f)

            href = product.css("section a::attr(href)").get()
            price = product.css(".styles_price__tiO8k span::text").get()
            name = product.css(".styles_title__XS_QS::text").get()
            date = product.css(".styles_secondary__dylmH p + span::text").get()
            data = f"{href}\n{price}\n{name}\n{date}\n"
            output.append(data)


                # f.write(img)
            count += 1
            if count > 3:
                break
        with open("test.txt", "w") as f:
            f.write("".join(output))


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(KufarSpider)
    process.start()
