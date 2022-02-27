import scrapy
from loguru import logger


class AmazonphonespiderSpider(scrapy.Spider):
    name = 'AmazonPhoneSpider'
    start_urls = ['https://www.amazon.in/s?k=phones']

    def parse(self, response):
        try:
            logger.info("Entering to parse the data")
            item = {}
            for job in response.xpath('.//a[@class="a-link-normal s-underline-text s'
                                      '-underline-link-text s-link-style a-text-normal"]/@href'):
                job = job.get()
                job = response.urljoin(job)
                yield scrapy.Request(job, meta={'item': item}, callback=self.detail)
        except Exception as e:
            logger.exception(f"Exception while parsing the data: {str(e)}")

    def detail(self, response):
        try:
            logger.info("Entering into detailed scrapping")
            item = response.meta.get('item')

            product_title = response.xpath(".//span[@id='productTitle']/text()").get()
            product_actual_price = response.xpath(".//span[@class='a-price a-text-price a-size-base']//text()").get()
            product_deal_price = response.xpath(".//span[@class='a-price a-text-price a-size-medium apexPriceToPay']"
                                                "//text()").get()
            about_the_item = response.xpath(".//h1[contains(text(), 'About this item')]/following-sibling::ul//"
                                            "text()").getall()
            item['productTitle'] = product_title.strip()
            if product_actual_price is not None:
                item['actualPrice'] = product_actual_price.replace(u"\u20b9", "")
            else:
                item['actualPrice'] = product_actual_price
            if product_deal_price is not None:
                item['dealPrice'] = product_deal_price.replace(u"\u20b9", "")
            else:
                item['dealPrice'] = product_deal_price
            for value in about_the_item:
                if value.strip() == "":
                    about_the_item.remove(value)
            item['aboutItem'] = about_the_item
            yield item
        except Exception as e:
            logger.exception(f"Exception while detailed scrapping: {str(e)}")
