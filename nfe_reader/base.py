
from requests import Session


class Crawler:
    state: str = None
    base_url: str = None

    def __init__(self):
        self.session = Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"  # noqa E501
            }
        )

    def search_by_qrcode(self, url):
        raise NotImplementedError()
