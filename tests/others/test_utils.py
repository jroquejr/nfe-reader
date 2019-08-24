import pytest

from nfe_reader.utils import get_parsed, parse_form
from tests.util import load_file


def test_get_parsed():
    html = "<html><body><h1>meu titulo</h1><div>Outro conteúdo</div></body></html>"
    parsed = get_parsed(html)
    assert parsed.find("h1").text == "meu titulo"


@pytest.mark.parametrize("fixture", ("parse_form/form1.html", "parse_form/form2.html"))
def test_parse_form(fixture, snapshot):
    html = load_file(fixture)
    parsed = get_parsed(html)
    form_data = parse_form(parsed.find("form"))
    snapshot.assert_match(form_data)
