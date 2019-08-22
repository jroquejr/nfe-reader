from tests.util import load_file
from pytest import fixture


@fixture(scope="module")
def html_first_page():
    return load_file("crawler_ba/fixture-first-page.html")


@fixture(scope="module")
def html_tabs_view():
    return load_file("crawler_ba/fixture-tabs-view.html")


@fixture(scope="module")
def html_emitter():
    return load_file("crawler_ba/emitter.html")


@fixture(scope="module")
def html_products():
    return load_file("crawler_ba/products.html")