import re
from decimal import Decimal

import dateparser
from superslug import slugify

from nfe_reader.utils import get_parsed
from nfe_reader.models import NFeModel


class Parser:
    def extract_by_css(self, content, selector, attribute="text"):
        element = content.select_one(selector)
        if element:
            return element.get(attribute)

    def parse(self, content) -> NFeModel:
        nfe_parsed = get_parsed(content.get("nfe"))
        nfe_dict = self.extract_nfe_as_dict(nfe_parsed)

        return NFeModel(
            {
                "access_key": self.extract_access_key(nfe_parsed),
                "number": nfe_dict.get("numero"),
                "issue_date": self.extract_issue_date(nfe_dict),
                "total_value": self.extract_total_value(nfe_dict),
            }
        )

    def extract_nfe_as_dict(self, parsed):
        label_list = parsed.select("#NFe tr td label")
        nfe_dict = {}
        for label in label_list:
            value_row = label.find_next("span")
            nfe_dict[slugify(label.text)] = value_row.text.strip()
        return nfe_dict

    def extract_access_key(self, nfe_parsed):
        result = nfe_parsed.select_one("#lbl_chave_acesso")
        if result:
            return re.sub(r"[^0-9]", "", result.text)

    def extract_issue_date(self, nfe_dict):
        result = nfe_dict.get("data-de-emissao")
        if result:
            return dateparser.parse(result)

    def extract_total_value(self, nfe_dict):
        result = nfe_dict.get("valor-total-da-nota-fiscal")
        if result:
            return Decimal(result.replace(",", "."))
