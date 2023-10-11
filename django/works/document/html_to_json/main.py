import json
import logging
from bs4 import BeautifulSoup
from works.document.html_to_json.utils import get_sub_items


class ParseHtml:
    """Class to convert html to json"""
    html = None
    json = None
    soup = None

    def __init__(self, html):
        try:
            if html is None:
                raise TypeError("The html parameter cannot be null.")

            self.html = html
            self.soup = BeautifulSoup(self.html, 'html.parser')
        except TypeError as error:
            logging.exception(f"ParseHtml.init - Error on initializing the class: {error}")
            self.html = None

    def set_html(self, html):
        """Method to set html input."""
        try:
            if html is None:
                raise TypeError("The html parameter cannot be null.")

            self.html = html
            self.soup = BeautifulSoup(self.html, 'html.parser')
        except TypeError as error:
            self.html = None

    def convert_to_json(self):
        """Method to convert html input to json output."""
        try:
            tags = self.soup.find_all(recursive=False)
        except Exception as error:
            logging.exception(f"ParseHtml.convert_to_json - Error: {error}")
        else:
            keys = get_sub_items(tags)
            self.json = json.dumps({"keys": keys}, indent=2, ensure_ascii=False)

            return self.json