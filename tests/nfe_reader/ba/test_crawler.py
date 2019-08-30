import re

import pytest
import requests_mock

from nfe_reader.ba.crawler import Crawler
from nfe_reader.exceptions import InvalidQRCode, UnavailableServerException
from tests.util import load_file

FAKE_URL = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=29190710230480000300650020046429391067584521|2|1|1|02DEF8AF9895079E1B6C439CD83A91A04E0F04E0"


def test_ba_crawler(html_first_page, html_nfe, html_emitter, html_products):
    with requests_mock.mock() as m:
        m.register_uri("GET", re.compile("qrcode.aspx"), text=html_first_page)
        m.register_uri("POST", re.compile("NFCEC_consulta_danfe.aspx"), text=html_nfe)
        m.register_uri(
            "POST",
            re.compile("NFCEC_consulta_abas.aspx"),
            [{"text": html_emitter}, {"text": html_products}],
        )

        crawler = Crawler()
        result = crawler.search_by_qrcode(FAKE_URL)
        assert result


def test_server_failed(html_server_error):
    with requests_mock.mock() as m:
        m.register_uri("GET", re.compile("qrcode.aspx"), text=html_server_error)
        crawler = Crawler()

        with pytest.raises(UnavailableServerException):
            crawler.search_by_qrcode(FAKE_URL)


@pytest.mark.parametrize(
    "fixture,exception_class",
    [
        ("crawler_ba/server-error.html", UnavailableServerException),
        ("crawler_ba/qrcode-error.html", InvalidQRCode),
    ],
)
def test_server_errors(fixture, exception_class):
    html = load_file(fixture)
    with requests_mock.mock() as m:
        m.register_uri("GET", re.compile("qrcode.aspx"), text=html)
        crawler = Crawler()
        with pytest.raises(exception_class):
            crawler.search_by_qrcode(FAKE_URL)
