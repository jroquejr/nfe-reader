import re

import requests_mock

from nfe_reader.ba.crawler import Crawler


def test_ba_crawler(html_first_page, html_tabs_view, html_emitter, html_products):
    with requests_mock.mock() as m:
        m.register_uri("GET", re.compile("qrcode.aspx"), text=html_first_page)
        m.register_uri(
            "POST", re.compile("NFCEC_consulta_danfe.aspx"), text=html_tabs_view
        )
        m.register_uri(
            "POST",
            re.compile("NFCEC_consulta_abas.aspx"),
            [{"text": html_emitter}, {"text": html_products}],
        )
        url_qrcode = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=29190710230480000300650020046429391067584521|2|1|1|02DEF8AF9895079E1B6C439CD83A91A04E0F04E0"

        crawler = Crawler()
        result = crawler.search_by_qrcode(url_qrcode)
        assert result
