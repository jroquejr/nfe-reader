import pytest

from nfe_reader.base import Crawler


def test_crawler_not_implemented():
    class NewCrawler(Crawler):
        pass

    with pytest.raises(NotImplementedError):
        NewCrawler().search_by_qrcode("")
