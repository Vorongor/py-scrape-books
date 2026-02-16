import scrapy


class ScrapeBooksPipeline:
    def process_item(
            self,
            item: scrapy.Item,
            spider: scrapy.Spider
    ) -> scrapy.Item:
        return item
