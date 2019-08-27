from furl import furl

from nfe_reader import base
from nfe_reader.exceptions import InvalidQRCode, UnavailableServerException
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
            content[name] = tab_response.text
        return self.parser.parse(content)

    def get_tabbed_content(self, url):
        first_page = self.session.get(url)
        self.check_return_from_server(first_page.text)
        parsed = get_parsed(first_page.text)
        form_element = parsed.find("form")
        form_data = parse_form(form_element)
        partial_url = form_element.get("action").replace("./", "")
        tabbed_page = self.session.post(
            furl(first_page.url).join(partial_url).url,
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return tabbed_page.text

    def check_return_from_server(self, html):
        if (
            "Ocorreu um erro no processamento da página: Problemas na leitura dos dados da NFC-e"
            in html
        ):
            raise UnavailableServerException()

        if (
            "Problema(s) apresentado(s) no QR Code" in html
            and "Versão do QR Code não preenchida" in html
        ):
            raise InvalidQRCode()
