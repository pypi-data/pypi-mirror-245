from ..classes.widget import Widget
from rich import print


class WidgetPrinter:

    @staticmethod
    def print_canvas(canvas: Widget):
        assert canvas.name == "canvas"
        lines = []
        WidgetPrinter.__print_recursive(canvas, indent=0, lines=lines)
        for line in lines:
            print(line)

    @staticmethod
    def __print_recursive(widget: Widget, indent: int, lines: list[str]):

        if isinstance(widget, list):
            lines.append(str(widget))
        else:

            if widget.name in ["canvas", "list", "list-item"]:

                lines.append("    " * indent + f"[purple]name[/]: {widget.name}")
                lines.append("    " * indent + f"attributes: {widget.attributes}")
                lines.append("    " * indent + f"content:")

                indent += 1
                for item in widget.content:
                    WidgetPrinter.__print_recursive(item, indent, lines)
                indent -= 1
            
            elif widget.name in ["label", "button", "entry"]:

                lines.append("    " * indent + f"[purple]name[/]: {widget.name}")
                lines.append("    " * indent + f"attributes: {widget.attributes}")
                lines.append("    " * indent + f"content: [blue]{widget.content}")
