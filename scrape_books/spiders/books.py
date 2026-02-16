from typing import Generator, Any

import scrapy
from scrapy.loader import ItemLoader
from scrape_books.items import ScrapeBooksItem
from scrapy.http import Response


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response: Response, **kwargs) -> Generator[Any, Any, None]:
        for book in response.css(".product_pod"):
            yield response.follow(
                book.css("h3 a::attr(href)").get(),
                callback=self._parse_details
            )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def _parse_details(self, response: Response) -> Generator[Any, Any, None]:
        loader = ItemLoader(item=ScrapeBooksItem(), response=response)

        loader.add_css("title", "h1::text")
        loader.add_css("price", ".price_color::text")
        loader.add_css("rating", ".star-rating::attr(class)")
        loader.add_xpath("upc",
                         "//th[text()='UPC']/following-sibling::td/text()")
        loader.add_css("category", ".breadcrumb li:nth-child(3) a::text")
        loader.add_css("stock_text", ".instock.availability::text")
        loader.add_css("description", "#product_description + p::text")

        yield loader.load_item()
