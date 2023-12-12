import os

cd = os.path.abspath(os.path.dirname(__file__))

XSD_FILE = os.path.join(cd, "xml_schema.xsd")
TEST_XML_FILE = os.path.join(cd, "test_xml.xml")
STYLE_LIGHT = os.path.join(cd, "pyStyle", "light.json")
STYLE_DARK = os.path.join(cd, "pyStyle", "dark.json")
