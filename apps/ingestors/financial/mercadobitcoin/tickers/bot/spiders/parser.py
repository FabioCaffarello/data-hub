from . import static
from baseparser import parser


class BotParser(parser.BaseParser):

    def __init__(self, *args, **kwargs) -> None:
        super(BotParser, self).__init__(*args, **kwargs)
        self.base_endpoint = static.BASE_ENDPOINT
        self.path_endpoint = static.PATH_ENDPOINT

    def _get_endpoint(self) -> str:
        return f"{self.base_endpoint}/{self.path_endpoint}"

    def generator_parse_data(self, raw_data):
        _data = list(filter(lambda x: x["name"] == "crypto", raw_data["categories"]))
        return ({"ticker": _d["symbol"]} for _d in _data[0]["assets"])
