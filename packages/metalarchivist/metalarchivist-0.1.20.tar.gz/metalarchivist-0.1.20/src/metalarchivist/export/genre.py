import time
import concurrent.futures

import urllib3
from rich.console import Console

from .util import MetalArchivesDirectory


class GenreError(Exception):
    def __init__(self, status_code, url):
        self.status_code = status_code
        self.url = url

    def __repr__(self):
        return self.__name__ + f'<{self.status_code}: {self.url}>'
