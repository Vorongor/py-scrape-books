import scrapy
from scrapy import Selector
from scrapy.http import Response


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    rating_exchange = {
        "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
    }

    def parse(self, response: Response, **kwargs):
        books = response.css(".product_pod")

        for book in books:
            detail_link = book.css("h3 a::attr(href)").get()
            yield response.follow(
                detail_link,
                callback=self._parse_details
            )

        nex_page = response.css(".next a::attr(href)").get()
        if nex_page is not None:
            nex_page_url = response.urljoin(nex_page)
            yield response.follow(nex_page_url, callback=self.parse)

    def _parse_details(self, response: Response):
        title = response.css("h1::text").get()
        price_text = response.css(".price_color::text").get()
        price = float(price_text.replace("£", ""))
        rating_classes = response.css(".star-rating::attr(class)").get()
        rating_key = rating_classes.replace("star-rating ", "")
        upc = response.xpath(
            "//th[text()='UPC']/following-sibling::td/text()").get()
        category = response.css(".breadcrumb li:nth-child(3) a::text").get()
        stock_text = response.css(".instock.availability::text").getall()
        stock_text = "".join(stock_text).strip()
        amount_in_stock = int("".join(filter(str.isdigit, stock_text)))

        yield {
            "title": title,
            "price": price,
            "rating": self.rating_exchange[rating_key],
            "amount_in_stock": amount_in_stock,
            "category": category,
            "description": response.css(
                "#product_description + p::text"
            ).get(),
            "upc": upc,
        }