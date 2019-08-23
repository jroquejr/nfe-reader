
from requests import Session


class Crawler:
    state: str = None
    base_url: str = None

    def __init__(self):
        self.session = Session()

    def search_by_qrcode(self, url):
        raise NotImplementedError()
