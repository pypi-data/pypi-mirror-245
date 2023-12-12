import os

with open(os.path.join(os.path.dirname(__file__), "xml_schema.xsd"), "r") as f:
    SCHEMA = f.read()
