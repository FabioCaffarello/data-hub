import os
import sys
import importlib
from botargparse import argparse
from botlog.log import log_config
from scrapy.utils.project import get_project_settings
from crawler import loop
import logging


def set_module_log_to_error(module):
    log = logging.getLogger(module)
    log.setLevel(logging.ERROR)


def run_crawler(spider_module, spider_class, concurrency, botname=None):
    log = logging.getLogger("basecrawler.run_crawler")
    spider_module = importlib.import_module(spider_module)
    SpiderClass = getattr(spider_module, spider_class)
    if botname is not None:
        SpiderClass.name = botname
    settings = get_project_settings()
    log.info("runnig loop")
    loop.run(SpiderClass, settings, concurrency)



def main():
    parser = argparse.new(description="Starts Base Crawler Daemon")
    parser.add_argument(
        "--crawler",
        help="Crawler to be executed"
    )
    parser.add_argument(
        "--botname",
        help="Override botname"
    )
    args = parser.parse_args()

    if args.crawler is None:
        print("--crawler is obligatory. run --help for more details")
        sys.exit(-1)

    print("basecrawler.init: Configuring log level: {}".format(args.log_level))
    log_config(args.log_level)
    log = logging.getLogger("basecrawler.init")
    log.info(
        "configured log level to '{}' with success. Starting loop".format(
            args.log_level
        )
    )

    spider_class = args.crawler.split(".")[-1]
    spider_module = args.crawler.split(".")[:-1]
    spider_module = ".".join(spider_module)

    log.info("running crawler")
    run_crawler(
        spider_module,
        spider_class,
        args.concurrency
        args.botname,
    )

    log.error("crawler stopped runnig, flushing logs")
    logging.shutdown()
    print("flushed logs, forcing exit with error")
    sys.stdout.flush()
    os._exit(-1)

if __name__ == "__main__":
    main()
