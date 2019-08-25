from bs4 import BeautifulSoup, Tag


def get_parsed(html, parser="html.parser"):
    return BeautifulSoup(html, parser)


def super_strip(text):
    return " ".join([t.strip() for t in text.splitlines()])


def force_float(text):
    return float(text.replace(",", ".")) if text else None


def parse_form(form_element: Tag):
    fields = {}

    def parse_input(element):
        fields[element.get("name")] = element.get("value", "")

    def parse_checked(element):
        if hasattr(element, "checked"):
            fields[element["name"]] = element.get("value", "on")

    def parse_textarea(element):
        fields[element.get("name")] = element.text or ""

    def parse_select(element):
        options = element.find_all("option")
        selected_options = element.find_all("option", {"selected": True})
        is_multiple = bool(element.has_attr("multiple"))

        if not selected_options and options:
            selected_options = [options[0]]

        values = [option.get("value", "") for option in selected_options]
        fields[element.get("name")] = values if is_multiple else values[0]

    for element in form_element.select("input,textarea,select"):
        element_type = element.get("type")

        if not hasattr(element, "name") or not element.get("name"):
            continue

        if element.name == "textarea":
            parse_textarea(element)
            continue

        if element.name == "select":
            parse_select(element)
            continue

        if element_type in ("checkbox", "radio"):
            parse_checked(element)
            continue

        if (
            element_type in ("text", "hidden", "password", "submit", "image")
            or not element_type
        ):
            parse_input(element)
            continue

    return fields
