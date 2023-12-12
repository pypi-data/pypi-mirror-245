import xml.sax
from .widget import Widget


class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.__widgets = []

        # for any widget that stores other widgets
        self.__active_names = []
        self.__active_attributes = []
        self.__active_contents = []

    def startElement(self, tag, attributes):
        if tag in ["canvas", "list", "list-item"]:
            self.__active_names.append(tag)
            self.__active_attributes.append(attributes)
            self.__active_contents.append([])
        elif tag in ["label", "button", "entry"]:
            self.__active_names.append(tag)
            self.__active_attributes.append(attributes)
            self.__active_contents.append("")

    def characters(self, content: str):
        if content.strip() == "":
            return
        self.__active_contents[-1] = self.__active_contents[-1] + content.strip()

    def endElement(self, name):
        w_name = self.__active_names.pop()
        w_attributes = dict(self.__active_attributes.pop())
        if name in ["canvas", "list"]:
            # for now only vertical canvases and lists are allowed
            w_attributes["pyAxis"] = "vertical"
        if name in ["label", "button", "entry"]:
            # w_attributes["anchor"] = "topleft" # ! not needed: done in StyleInserter
            pass
        if name == "list-item":
            # for now list-items are always horizontal
            w_attributes["pyAxis"] = "horizontal"
        w_content = self.__active_contents.pop()
        widget = Widget(w_name, w_attributes, w_content)
        if name == "canvas":
            self.__widgets.append(widget)
        else:
            self.__active_contents[-1].append(widget)

    def get_widget_structure(self):
        return self.__widgets
