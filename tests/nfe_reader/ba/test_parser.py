from nfe_reader.ba.parser import Parser


def test_parser(html_tabs_view, html_emitter, html_products, snapshot):
    parser = Parser()
    nfe = parser.parse(
        {"nfe": html_tabs_view, "emitter": html_emitter, "products": html_products}
    )
    snapshot.assert_match(nfe.to_primitive())
