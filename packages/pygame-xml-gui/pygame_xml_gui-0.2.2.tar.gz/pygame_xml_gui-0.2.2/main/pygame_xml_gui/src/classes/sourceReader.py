import os
from .widget import Widget


class SourceReader:
    """
    SourceReader only needs to run if the GUI is being tested with example
    data from a file. In production, the local variables will be supplied
    by the parent program.
    """

    def __init__(self, widgets: list[Widget]):
        self.__widgets = widgets
        self.__sanity_check()
        self.__source = self.__widgets[0].attributes.get("pySource", None)
        self.__vars = {}
        self.__import_source()
    
    def get_variables(self):
        return self.__vars

    def __sanity_check(self):
        assert len(self.__widgets) == 1
        assert self.__widgets[0].name == "canvas"

    def __import_source(self):
        if self.__source == None:
            return

        # checking for errors
        s = os.path.abspath(self.__source)
        if not os.path.exists(s):
            raise Exception(f"Source file does not exist ({s})")
        if not os.path.isfile(s):
            raise Exception(f"Given source file is not a file ({s})")
        if not (str(s).endswith(".py") or str(s).endswith(".pyw")):
            raise Exception(f"Given source file has to be a python file (.py or .pyw)")

        # trying to load the variables
        try:
            with open(self.__source, "r") as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Could not find source file ('{self.__source}')")
        try:
            exec(
                "import warnings\nwarnings.filterwarnings('ignore')\n" + code,
                None,
                self.__vars,
            )
        except Exception as e:
            raise Exception(f"Error executing source file: {e}")
