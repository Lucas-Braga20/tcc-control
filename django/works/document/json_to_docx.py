import json

from bs4 import BeautifulSoup
from docxtpl import DocxTemplate

from works.document.html_to_json.script import convert
from works.document.html_to_docx.main import HTMLtoDocx


def is_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return bool(soup.find())


class JsonToDocx:
    def __init__(self, input_path_docx, json_data, output_path_docx):
        self.input_path_docx = input_path_docx
        self.json_data = json_data
        self.output_path_docx = output_path_docx
        self.doc = DocxTemplate(input_path_docx)
        self.html2docx = HTMLtoDocx(self.doc)

    def convert(self):
        context = {}

        for field in self.json_data.get("fields", []):
            key = field.get("key")
            value = field.get("value")

            if key and value:
                if is_html(value):
                    try:
                        json_string = convert(value)
                        items = json.loads(json_string)
                        context[key] = self.html2docx.convert(items)
                    except Exception as e:
                        print(f"Erro ao converter HTML para JSON: {str(e)}")

                        return None
                else:
                    context[key] = value

        try:
            self.doc.render(context)
            self.doc.save(self.output_path_docx)

            return self.output_path_docx
        except Exception as e:
            print(f"Erro ao criar o documento: {str(e)}")

            return None
