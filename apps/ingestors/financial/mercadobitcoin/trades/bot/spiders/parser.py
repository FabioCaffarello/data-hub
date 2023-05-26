from . import static
from baseparser import parser


class BotParser(parser.BaseParser):

    def __init__(self, *args, **kwargs) -> None:
        super(BotParser, self).__init__(*args, **kwargs)
        self.base_endpoint = static.BASE_ENDPOINT
        self.path_endpoint = static.PATH_ENDPOINT

    def _get_endpoint(self) -> str:
        return f"{self.base_endpoint}/{self.path_endpoint}"
