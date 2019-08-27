import re
from decimal import Decimal

import dateparser
from superslug import slugify

from nfe_reader.models import EmitterModel, NFeModel, ProductModel
from nfe_reader.utils import force_float, get_parsed, super_strip


class Parser:
    def parse(self, content) -> NFeModel:
        parsed_content = {k: get_parsed(v) for k, v in content.items()}

        nfe_dict = {}
        nfe_dict.update(
            self.extract_as_dict(parsed_content["nfe"].select("#NFe tr td label"))
        )
        nfe_dict.update(
            self.extract_as_dict(
                parsed_content["emitente"].select("#Emitente tr td label")
            )
        )

        city_parts = nfe_dict.get("municipio").split("-")

        return NFeModel(
            {
                "access_key": self.extract_access_key(parsed_content.get("nfe")),
                "number": nfe_dict.get("numero"),
                "issue_date": self.extract_issue_date(nfe_dict),
                "total_value": force_float(nfe_dict.get("valor-total-da-nota-fiscal")),
                "emitter": EmitterModel(
                    {
                        "name": nfe_dict.get("nome-razao-social"),
                        "fantasy_name": nfe_dict.get("nome-fantasia"),
                        "cnpj": self.only_numbers(nfe_dict.get("cnpj")),
                        "state_reg": self.only_numbers(
                            nfe_dict.get("inscricao-estadual")
                        ),
                        "address": super_strip(nfe_dict.get("endereco", "")),
                        "district": nfe_dict.get("bairro-distrito"),
                        "uf": nfe_dict.get("uf"),
                        "zipcode": self.only_numbers(nfe_dict.get("cep")),
                        "city_code": city_parts[0].strip(),
                        "city_name": city_parts[1].strip(),
                    }
                ),
                "products": self.extract_products(parsed_content.get("produtos")),
            }
        )

    def extract_by_css(self, content, selector, attribute="text"):
        element = content.select_one(selector)
        if element:
            return element.get(attribute)

    def extract_as_dict(self, rows):
        nfe_dict = {}
        for label in rows:
            value_row = label.find_next("span")
            nfe_dict[slugify(label.text)] = value_row.text.strip()
        return nfe_dict

    def only_numbers(self, value):
        return re.sub(r"[^0-9]", "", value)

    def extract_access_key(self, nfe_parsed):
        result = nfe_parsed.select_one("#lbl_chave_acesso")
        if result:
            return self.only_numbers(result.text)

    def extract_issue_date(self, nfe_dict):
        result = nfe_dict.get("data-de-emissao")
        if result:
            return dateparser.parse(result)

    def extract_total_value(self, nfe_dict):
        result = nfe_dict.get("valor-total-da-nota-fiscal")
        if result:
            return Decimal(result.replace(",", "."))

    def extract_products(self, parsed):
        products = []
        for row in parsed.select(".table_produtos"):
            product = self.extract_product(row)
            if product:
                products.append(product)
        return products

    def extract_product(self, element):
        rows = element.select("table tr td label")
        product_dict = self.extract_as_dict(rows)
        return ProductModel(
            {
                "description": product_dict.get("descricao"),
                "quantity": force_float(product_dict.get("qtd")),
                "business_unity": product_dict.get("unidade-comercial"),
                "total_value": force_float(product_dict.get("valor-r")),
                "unit_value": force_float(
                    product_dict.get("valor-unitario-de-comercializacao")
                ),
                "product_code": product_dict.get("codigo-do-produto"),
                "ncm_code": product_dict.get("codigo-ncm"),
                "cfop": product_dict.get("cfop"),
                "total_tax": force_float(product_dict.get("valor-aproximado-dos-tributos")),
                "metadata": {
                    "code_anp": product_dict.get("codigo-do-produto-da-anp"),
                    "uf": product_dict.get("uf-de-consumo"),
                },
            }
        )
