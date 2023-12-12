class XMLHelper:
    @staticmethod
    def read_bool(xml_boolean: str) -> bool:
        if xml_boolean == "false" or xml_boolean == "0":
            return False
        elif xml_boolean == "true" or xml_boolean == "1":
            return True
        else:
            raise Exception(f"Unable to read xsd:boolean '{xml_boolean}'")