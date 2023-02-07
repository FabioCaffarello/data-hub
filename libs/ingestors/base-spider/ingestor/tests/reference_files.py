import json
import os

from ingestor import settings


def load(file_name):
    """Loads given file_name as array of bytes.
    """
    _path_debug = _absolute_path(file_name)
    with open(_path_debug, "rb") as file:
        return file.read()


def load_text(file_name, encoding="utf-8"):
    """Loads given file_name as text.
    """
    _path_debug = _absolute_path(file_name)
    with open(_path_debug, "r", encoding=encoding) as file:
        return file.read()


def load_json(file_name, encoding="utf-8"):
    """Loads given file_name as text.
    """
    return json.loads(load_text(file_name, encoding))


def _absolute_path(file_name):
    return os.path.realpath(
        os.path.join(
            settings.PATH_REFERENCE_FILES_DEBUG,
            file_name
        )
    )
