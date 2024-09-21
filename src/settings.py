import os
import json

import pygame as pg
pg.init()

FONTDIR = os.path.join("data", "fonts")
ICONDIR = os.path.join("data", "icons")

WIN_WIDTH = 900
WIN_HEIGHT = 700

ID_ACTION = {
    "MainMenu": {
        0: "Quit",
        1: "PlayMenu",
        2: "MusicMenu",
        3: "SettingsMenu"
    },
    "PlayMenu": {
        1: "Hum_vs_Hum",
        2: "Hum_vs_ROB",
        3: "Timer",
        0: "Back",
    }
}


def load_config(path):
    with open(path, "r") as f:
        return json.load(f)


LAYOUT_INFO = load_config("layout.json")
OPTIONS = load_config("settings.json")

THEME = {
    "font": pg.font.Font(f"{FONTDIR}/FiraCode-SemiBold.ttf", 20),
    "tcolor": OPTIONS["button"]["text"],
    "bcolor": OPTIONS["button"]["background"],
    "s_bcolor": OPTIONS["button"]["sbackground"],
}
