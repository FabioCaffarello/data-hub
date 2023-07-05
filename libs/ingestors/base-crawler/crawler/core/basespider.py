import json
import os
from abc import abstractmethod

import scrapy
from crawler import settings


class BaseSpider(scrapy.Spider):
    # def __init__(self, rabbitmq_middleware=None, *args, **kwargs):
    def __init__(self, input_msg, rabbitmq_middleware=None, *args, **kwargs):
        self.logger.info(f"Creating spider to crawl: {input_msg}")
        super(BaseSpider, self).__init__(*args, **kwargs)
        self._input_data = input_msg
        # self.rabbitmq_middleware = rabbitmq_middleware
        requests = self.start_requests()
        self.__start_requests = []
        self.eos = None
        if requests is not None:
            try:
                for r in requests:
                    self.__start_requests.append(r)
            except TypeError:
                self.__start_requests.append(requests)
        self.logger.info("Spider creation completed with success")

    @abstractmethod
    def start_requests(self):
        raise NotImplementedError()

    def debug_response(self, file_name, content):
        _path_debug = os.path.realpath(
            os.path.join(
                settings.PATH_DEBUG,
                'response',
                file_name
            )
        )
        _extension = file_name.split(".")[-1]

        if _extension == "json":
            with open(_path_debug, "wb") as file:
                file.write(json.dumps(content, indent=4).encode("utf-8"))
            return
        with open(_path_debug, "wb") as file:
            file.write(content)
        return