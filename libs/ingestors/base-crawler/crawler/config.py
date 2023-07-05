import logging

from crawler import settings
from scrapy.utils.log import configure_logging


class LoggingConfig:
    def __init__(self):
        configure_logging(install_root_handler=False)
        logging.basicConfig(
            filename=f'{settings.PATH_DEBUG}/log.txt',
            filemode='w',
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )
