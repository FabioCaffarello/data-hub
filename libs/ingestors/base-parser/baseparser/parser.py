from abc import ABC, abstractmethod

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class BaseParser(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def _get_endpoint(self, *args, **kwargs) -> str:
        raise NotImplementedError()
