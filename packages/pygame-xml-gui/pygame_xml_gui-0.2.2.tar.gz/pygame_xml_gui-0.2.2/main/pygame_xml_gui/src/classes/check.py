import os
import sys
from rich import print as rprint

class Check:

    @staticmethod
    def xml_path(path):
        if not os.path.exists(path):
            rprint(f"[red]Path does not exist: {path}")
            sys.exit()
        if not os.path.isfile(path):
            rprint(f"[red]Path is not a file: {path}")
            sys.exit()
    
    @staticmethod
    def output_path(path):
        if not (path.endswith(".py") or path.endswith(".pyw")):
            rprint(f"[red]Destination path has to be a python file (.py or .pyw)")
            sys.exit()
