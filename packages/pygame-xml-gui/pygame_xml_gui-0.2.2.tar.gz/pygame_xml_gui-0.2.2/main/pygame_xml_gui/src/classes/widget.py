class Widget:
    def __init__(self, name: str, attributes: dict, content):
        self.name = name
        self.attributes = attributes
        self.content = content

        self.__info = {}

    def set_width(self, width):
        self.__info["force_width"] = width

    def set_height(self, height):
        self.__info["force_height"] = height

    def __repr__(self) -> str:
        content = "\"" + self.content + "\"" if isinstance(self.content, str) else self.content
        return f"Widget(name='{self.name}', attributes={dict(self.attributes)},content={content})"