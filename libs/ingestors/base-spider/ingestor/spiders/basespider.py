import json
import os
from abc import abstractmethod

import scrapy
# import yaml
from ingestor import settings


class BaseSpider(scrapy.Spider):
    def __init__(self, input_msg, *args, **kwargs):
        self.logger.info(f"Creating spider to crawl: {input_msg}")
        super(BaseSpider, self).__init__(*args, **kwargs)
        self._input_data = input_msg
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
        # elif _extension == "yaml" or _extension == "yml":
        #     with open(_path_debug, "w") as file:
        #         yaml.dump(yaml.safe_load(content), file)
        #     return
        with open(_path_debug, "wb") as file:
            file.write(content)
        return
