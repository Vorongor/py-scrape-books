import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def extract_rating(value: str) -> int:
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    key = value.replace("star-rating ", "").strip()
    return rating_map.get(key, 0)


def parse_price(value: str) -> float:
    return float(value.replace("£", ""))


def parse_stock(value: str) -> int:
    return int("".join(filter(str.isdigit, value)))


class ScrapeBooksItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(
        input_processor=MapCompose(parse_price),
        output_processor=TakeFirst()
    )
    rating = scrapy.Field(
        input_processor=MapCompose(extract_rating),
        output_processor=TakeFirst()
    )
    upc = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    amount_in_stock = scrapy.Field(
        input_processor=MapCompose(parse_stock),
        output_processor=TakeFirst()
    )
