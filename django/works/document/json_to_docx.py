import json
import win32com.client

from bs4 import BeautifulSoup
from docxtpl import DocxTemplate

from html2json.script import convert
from html2docx.main import HTMLtoDocx


def is_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return bool(soup.find())


def docx2pdf(path_docx, path_pdf):
    word = win32com.client.Dispatch('Word.Application')
    doc = word.Documents.Open(path_docx)
    try:
        doc.SaveAs(path_pdf, FileFormat=17)
    except Exception as e:
        print(f"Erro ao converter para PDF: {str(e)}")
    finally:
        doc.Close()
        word.Quit()


class JsonToDocx:
    def __init__(self, input_path_docx, json_data, output_path_docx, output_path_pdf):
        self.input_path_docx = input_path_docx
        self.json_data = json_data
        self.output_path_docx = output_path_docx
        self.output_path_pdf = output_path_pdf
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
                else:
                    context[key] = value

        try:
            self.doc.render(context)
            self.doc.save(self.output_path_docx)
            docx2pdf(self.output_path_docx, self.output_path_pdf)
        except Exception as e:
            print(f"Erro ao criar o documento: {str(e)}")
