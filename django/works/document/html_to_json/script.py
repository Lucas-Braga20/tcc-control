from works.document.html_to_json.main import ParseHtml


def convert(html_content):
    parse_html = ParseHtml(html=html_content)
    json_content = parse_html.convert_to_json()
    return json_content