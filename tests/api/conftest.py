from pytest import fixture

from api.app import create_app


@fixture(scope="module")
def app():
    return create_app({"TESTING": True})


@fixture(scope="module")
def client(app):
    return app.test_client()


@fixture(scope="module")
def nf_data():
    return {
        "access_key": "29190734274233001508650060001843241156013508",
        "emitter": {
            "address": "EDISTIO PONDE, 474",
            "city_code": "2927408",
            "city_name": "Salvador",
            "cnpj": 34274233001508,
            "district": "STIEP",
            "fantasy_name": "",
            "name": "PETROBRAS DISTRIBUIDORA S A",
            "state_reg": 57489368,
            "uf": "BA",
            "zipcode": 41770395,
        },
        "issue_date": "2019-04-07T18:43:47.000000-0300",
        "number": "184324",
        "products": [
            {
                "business_unity": "L",
                "cfop": "5656",
                "description": "GASOLINA COMUM C",
                "metadata": {"code_anp": "320102001", "uf": "BA"},
                "ncm_code": "27101259",
                "product_code": "0000000010101",
                "quantity": 11.313,
                "total_tax": 22.72,
                "total_value": 50.0,
                "unit_value": 4.42,
            }
        ],
        "protocol": None,
        "total_value": 50.0,
    }
