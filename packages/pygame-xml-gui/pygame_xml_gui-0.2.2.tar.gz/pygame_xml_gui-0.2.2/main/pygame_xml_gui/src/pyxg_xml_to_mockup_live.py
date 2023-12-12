import argparse
import os
import sys
import time

import xml.sax
import pygame
import PygameXtras as pe

from rich import print as rprint

from classes.validator import Validator
from classes.xmlHandler import XMLHandler
from classes.sourceInserter import SourceInserter
from classes.styleInserter import StyleInserter
from classes.sizeInserter import SizeInserter
from classes.guiMaker import GUIMaker

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path of the xml file to create a mockup from")
parser.add_argument("dest", help="Path of the mockup file")

args = parser.parse_args()
xml_path = os.path.abspath(args.path)
dest_path = os.path.abspath(args.dest)

if not os.path.exists(xml_path):
    print(f"Path does not exist: {xml_path}")
    sys.exit()
if not os.path.isfile(xml_path):
    print(f"Path is not a file: {xml_path}")
    sys.exit()

if not (dest_path.endswith(".py") or dest_path.endswith(".pyw")):
    print(f"Destination path has to be a python file (.py or .pyw)")
    sys.exit()

print(f"XML path: {xml_path}")
print(f"Output path: {dest_path}")

def get_info():
    Validator(xml_path)

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    handler = XMLHandler()
    parser.setContentHandler(handler)
    parser.parse(xml_path)

    widgets = SourceInserter(handler.get_widgets()).get_widgets()

    StyleInserter(widgets)

    SizeInserter(widgets)

    guiMaker = GUIMaker(widgets)
    return guiMaker.get_size(), guiMaker.get_widgets()

old_xml_text = ""

pygame.init()
screen = pygame.display.set_mode((100,100))
pygame.display.set_caption("Mockup")
fpsclock = pygame.time.Clock()
fps = 60

seconds_between_refresh = 1
last_refresh = 0
widgets = []
valid = True

while True:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if time.time() - last_refresh > seconds_between_refresh:
        last_refresh = time.time()
        with open(xml_path, "r") as f:
            xml_text = f.read()
        if xml_text != old_xml_text:
            try:
                screen_size, widgets = get_info()
                screen = pygame.display.set_mode(screen_size)
                if valid == False:
                    rprint("[green]Valid")
                valid = True
            except Exception as e:
                if valid:
                    rprint("[red]Invalid xml file:")
                    print(e)
                    valid = False
    
    for widget in widgets:
        if isinstance(widget, pe.Button):
            if widget.update(events):
                print(f"Pressed button with text '{widget.text}'")
    
    for widget in widgets:
        widget.draw_to(screen)

    pygame.display.flip()
    fpsclock.tick(fps)
