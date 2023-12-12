import re
import copy

from rich import print
from .widget import Widget

REGULAR_EXPRESSION = r"{{.*?}}"


class SourceInserter:
    def __init__(self, widgets: list[Widget], variables):
        self.__widgets = widgets
        self.__new_widgets = []

        self.__sanity_check()
        self.__vars = variables
        self.__run()

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"

    def __join_dicts(self, inferior: dict, superior: dict | None) -> dict:
        if superior is None:
            return inferior
        # new_dict = inferior.copy() # TODO: which one?
        new_dict = copy.deepcopy(inferior)
        for k, v in superior.items():
            new_dict[k] = v
        return new_dict

    def __run(self):
        self.__new_widgets = [
            self.__run_recursive(widget, {}) for widget in self.__widgets
        ]
        self.__unpack_lists()

    def __run_recursive(self, widget: Widget, additional_variables: dict):
        try:
            if bool(eval(widget.attributes.get("pyIf", "True"), None, self.__join_dicts(self.__vars, additional_variables))) == False:
                return None
        except Exception as e:
            raise Exception(f"An error occurred while evaluating the pyIf attribute of a widget (type: {widget.name}, "
                            + f"pyIf: '{widget.attributes.get('pyIf')}', exception: {e})")

        if widget.name in ["canvas", "list"]:
            return Widget(
                widget.name,
                widget.attributes,
                [
                    self.__run_recursive(item, additional_variables)
                    for item in widget.content
                ],
            )
        elif widget.name in ["label", "button", "entry"]:
            return self.__evaluate_widget(
                widget, additional_variables
            )
        elif widget.name == "list-item":
            return_list = []
            v1 = widget.attributes["pyFor"].split(" in ")[0]  # name of the iterable
            v2 = self.__vars[
                widget.attributes["pyFor"].split(" in ")[1]
            ]  # list of items to iterate over

            for variable_value in v2:
                content = []
                for widget_in_list_item in widget.content:
                    if (widget_ := self.__run_recursive(widget_in_list_item, {v1: variable_value})) is not None:
                        content.append(widget_)
                return_list.append(content)
            return [
                Widget(
                    widget.name,
                    {  # removes pyFor attribute
                        k: v for k, v in dict(widget.attributes).items() if k != "pyFor"
                    },
                    collection,
                )
                for collection in return_list
            ]

    def __unpack_lists(self):
        self.__unpacked_widgets = [
            self.__unpack_recursive(widget) for widget in self.__new_widgets
        ]
        self.__new_widgets = self.__unpacked_widgets

    def __unpack_recursive(self, widget: Widget) -> Widget | None:
        if widget.name in ["label", "button", "entry"]:
            return widget

        if widget.name in ["canvas", "list-item", "list"]:
            new_content = []
            for item in widget.content:
                if isinstance(item, list):
                    for i in item:
                        if i is not None:
                            new_content.append(i)
                else:
                    if item is not None:
                        new_content.append(self.__unpack_recursive(item))
            return Widget(widget.name, widget.attributes, new_content)

    def __evaluate_widget(self, widget: Widget, additional_locals: dict | None = None) -> Widget:
        assert widget.name in ["label", "button", "entry"]

        new_widget_attributes = copy.deepcopy(widget.attributes)
        string = widget.content

        vars_ = self.__join_dicts(self.__vars, additional_locals)

        for match in re.findall(REGULAR_EXPRESSION, string, re.DOTALL):
            to_be_evaluated = match[2:-2]
            evaluation = ""
            if to_be_evaluated.strip() != "":
                try:
                    evaluation = eval(to_be_evaluated, None, vars_)
                except Exception as e:
                    raise Exception(
                        f"An error occurred while evaluating the content of a widget (type: {widget.name}, original content: '{widget.content}')"
                        + f"\nContent to be evaluated: '{to_be_evaluated}'\nException: {e}"
                    )
            string = string.replace(match, str(evaluation))

        # adding the context (the local variables of the pyFor) to the attributes
        new_widget_attributes["contextInfo"] = additional_locals

        # evaluating pyArgs for button
        if widget.name == "button" and widget.attributes.get("pyArgs", False):
            raw_pyArgs = widget.attributes["pyArgs"]
            try:
                pyArgs = eval(raw_pyArgs, None, vars_)
            except Exception:
                raise Exception(
                    f"An error occurred while evaluating attribute 'pyArgs' for a widget (type: {widget.name}, content: '{widget.content}')"
                    + f"\nContent to be evaluated: '{raw_pyArgs}'"
                )
            new_widget_attributes["pyArgs"] = pyArgs


        return Widget(widget.name, new_widget_attributes, string)

    def get_widgets(self):
        return self.__new_widgets
