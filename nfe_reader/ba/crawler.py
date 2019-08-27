from furl import furl

from nfe_reader import base
from nfe_reader.utils import get_parsed, parse_form

from .parser import Parser


class Crawler(base.Crawler):
    state = "BA"
    base_url = "http://nfe.sefaz.ba.gov.br/"
    parser = Parser()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tab_search = furl(self.base_url).join(
            "/servicos/nfce/Modulos/Geral/NFCEC_consulta_abas.aspx"
        )

    def search_by_qrcode(self, url):
        tabbed_page = self.get_tabbed_content(url)
        content = {"nfe": tabbed_page}
        parsed = get_parsed(tabbed_page)
        form_data = parse_form(parsed.select_one("form"))
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
            tab_response.raise_for_status()
            content[name] = tab_response.text
        return self.parser.parse(content)

    def get_tabbed_content(self, url):
        first_page = self.session.get(url)
        first_page.raise_for_status()
        parsed = get_parsed(first_page.text)
        form_element = parsed.find("form")
        form_data = parse_form(form_element)
        partial_url = form_element.get("action").replace("./", "")
        tabbed_page = self.session.post(
            furl(first_page.url).join(partial_url).url,
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        tabbed_page.raise_for_status()
        return tabbed_page.text
