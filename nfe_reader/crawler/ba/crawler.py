from furl import furl

from nfe_reader.crawler import base
from nfe_reader.crawler.utils import get_parsed, parse_form


class Crawler(base.Crawler):
    state = "BA"
    base_url = "http://nfe.sefaz.ba.gov.br/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tab_search = furl(self.base_url).join(
            "/servicos/nfce/Modulos/Geral/NFCEC_consulta_abas.aspx"
        )

    def search_by_qrcode(self, url):
        tabbed_page = self.get_tabbed_content(url)
        content = {"nfe": tabbed_page}
        parsed = get_parsed(tabbed_page)
        form_data = parse_form(parsed.select_one("Form"))
        tab_list = [("emitente", 27, 10), ("produtos", 64, 7)]
        for name, x, y in tab_list:
            post_data = dict(form_data)
            post_data[f"btn_aba_{name}.x"] = x
            post_data[f"btn_aba_{name}.y"] = y
            tab_response = self.session.post(
                self.tab_search,
                data=post_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            content[name] = tab_response.text

    def get_tabbed_content(self, url):
        first_page = self.session.get(url)
        parsed = get_parsed(first_page.html)
        form_element = parsed.select_one("#form1")
        form_data = parse_form(form_element)
        tabbed_page = self.session.post(
            furl(self.base_url).join(form_element.get("action")).url, data=form_data
        )
        return tabbed_page.text
