class XmlAttributeValidator:
    def __init__(self):
        pass

    @staticmethod
    def check(attributeName: str, attributeValue):
        an, av = attributeName, attributeValue

        if an == "pyFor":
            return XmlAttributeValidator.__check_pyFor(av)

    @staticmethod
    def __check_pyFor(value):
        if not isinstance(value, str): return False
        if value.count(" in ") != 1: return False
        v1, v2 = value.split(" in ")
        if v1 == v2: return False
        
        return True

