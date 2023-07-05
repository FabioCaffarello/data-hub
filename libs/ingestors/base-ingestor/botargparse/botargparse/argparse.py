import argparse


def new(description):
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "--log-level",
        help="Sets the log level. Values: DEBUG,INFO,WARNING",
        dest="log_level",
        default="INFO"
    )

    parser.add_argument(
        "--concurrency",
        help="Sets concurrency level (amount of concurrent bots)",
        dest="concurrency",
        default=1
    )

    return parser
