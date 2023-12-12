#!python3

import sys
import os
import xmlschema

from xml.sax.handler import ContentHandler
from xml.sax import make_parser

# from files.paths import TEST_XML_FILE, XSD_FILE
from rich import print as rprint

# class Validator:
#     def __init__(self, path):
#         """This class validates the form of the xml file and its structure.\nCommand: pyxg_validate_xml {path_to_file}"""
#         self.path = path

#         self.check_form()
#         self.check_valid()

#     def check_form(self):
#         """Checks if the xml file is well-formed"""
#         parser = make_parser()
#         parser.setContentHandler(ContentHandler())
#         try:
#             parser.parse(self.path)
#         except Exception as e:
#             raise e

#     def check_valid(self):
#         """Checks if the xml file is valid against the schema"""
#         try:
#             xmlschema.validate(self.path, XSD_FILE)
#         except Exception as e:
#             raise e

class Validator:
    def __init__(self, structure, schema):
        """This class validates the form of the xml file and its structure.\nCommand: pyxg_validate_xml {path_to_file}"""

        self.structure = structure
        self.schema = schema

        self.check()

    def check(self):
        """Checks if the xml file is valid against the schema"""
        try:
            xmlschema.validate(self.structure, self.schema)
        except Exception as e:
            raise e
