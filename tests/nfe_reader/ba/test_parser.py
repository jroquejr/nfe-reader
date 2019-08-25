from nfe_reader.ba.parser import Parser


def test_parser(html_nfe, html_emitter, html_products, snapshot):
    parser = Parser()
    nfe = parser.parse(
        {"nfe": html_nfe, "emitente": html_emitter, "produtos": html_products}
    )
    snapshot.assert_match(nfe.to_primitive())
