import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class BotLoader(ItemLoader):
    default_output_processor = TakeFirst()

    def add_fields(self, fields):
        for key, value in fields.items():
            globals()[f"{key}"] = value
        self.add_value("ticker", ticker)
        pass


class BotItem(scrapy.Item):
    ticker = scrapy.Field()
    pass
