import json

from ..files.paths import STYLE_LIGHT, STYLE_DARK
from .widget import Widget

STYLES = {}

with open(STYLE_LIGHT, "r") as f:
    STYLES["light"] = json.load(f)

with open(STYLE_DARK, "r") as f:
    STYLES["dark"] = json.load(f)

class StyleInserter:
    def __init__(self, widgets: list[Widget]):
        self.__widgets = widgets

        self.__sanity_check()
        self.__style: dict = STYLES[self.__widgets[0].attributes["pyStyle"]]

        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"
        assert self.__widgets[0].attributes["pyStyle"] in STYLES.keys()

    def __run(self):
        self.__widgets = [
            self.__run_recursive(widget) for widget in self.__widgets
        ]

    def __run_recursive(self, widget: Widget):
        if widget.name in ["label", "button", "entry"]:
            return self.__get_widget_with_injected_style_attributes(widget)
        elif widget.name in ["canvas", "list", "list-item"]:
            return Widget(
                widget.name,
                widget.attributes,
                [
                    self.__run_recursive(item) for item in widget.content
                ]
            )

    def __get_widget_with_injected_style_attributes(self, widget: Widget) -> Widget:
        pyStyle_attributes = self.__extract_style_attribute(widget)

        attributes = widget.attributes
        for k, v in self.__style.items():
            if k not in attributes.keys():
                attributes[k] = v
        for k, v in pyStyle_attributes.items():
            attributes[k] = v
        attributes["anchor"] = "topleft"

        return Widget(widget.name, attributes, widget.content)

    def __extract_style_attribute(self, widget: Widget):
        if "pyStyle" in widget.attributes.keys():
            string = widget.attributes["pyStyle"]
            styles = string.split(";")
            styles = [s.strip() for s in styles if s.strip() != ""]
            styles_dict = {}
            for style in styles:
                try:
                    key = style.split("=")[0]
                    value = eval(style.split("=")[1])
                    styles_dict[key] = value
                except NameError:
                    raise Exception(f"Could not interpret key-value pair: {style}. Maybe you forgot quotation marks or a semicolon?")
                except:
                    raise Exception(f"Could not interpret key-value pair: {style}")
            return styles_dict
        return {}
