from bs4 import BeautifulSoup, Tag

def get_parsed(html, parser="html.parser"):
    return BeautifulSoup(html, parser)

def parse_form(form_element: Tag):
    fields = {}

    def parse_input(element):
        fields[element.get("name")] = element.get("value", "")

    def parse_checked(element):
        if "checked" in element:
            fields[element["name"]] = element.get("value", "on")

    def parse_textarea(element):
        fields[element.get("name")] = element.text or ""

    def parse_select(element):
        value = element.get("value")
        options = element.find_all("option")
        is_multiple = bool("multiple" in element)
        selected_options = [option for option in options if "selected" in option]

        if not selected_options and options:
            selected_options = [options[0]]

        if not is_multiple:
            value = selected_options[0].get("value", "")
        else:
            value = [option.get("value", "") for option in selected_options]
        fields[element.get("name")] = value

    for element in form_element.select("input,textarea,select"):
        element_type = element.get("type")

        if not hasattr(element, "name"):
            continue

        if element_type in ("text", "hidden", "password", "submit", "image") or not element_type:
            parse_input(element)
            continue

        if element_type in ("checkbox", "radio"):
            parse_checked(element)
            continue

        if element_type in ("textarea"):
            parse_textarea(element)
            continue

        if element_type in ("select"):
            parse_select(element)
            continue

    return fields