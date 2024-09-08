import os
import sys
import json

import pygame as pg

FONTDIR = os.path.join("data", "fonts")
ICONDIR = os.path.join("data", "icons")

WIN_WIDTH = 800 
WIN_HEIGHT = 600

ID_ACTION = {
    0:"Quit",
    1:"PlayMenu",
    2:"MusicMenu",
    3:"SettingsMenu"
}


def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

def quit():
    pg.quit()
    sys.exit()

LAYOUT_INFO = load_config("layout.json")
OPTIONS = load_config("settings.json")

EVENT_ACTION = {
        "PlayMenu": print,
        "MusicMenu": print,
        "SettingsMenu": print,
        "Quit": quit
}

EVENT_ARG = {
    "PlayMenu": "We are going to play",
    "MusicMenu": "Chill",
    "SettingsMenu": "no settings",
    "Quit":None 
}

