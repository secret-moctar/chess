import json
import os

from src.settings import *


class ConfigManager:
    def __init__(self):
        self.layouts = self.load_json(os.path.join("setup", "layout.json"))
        self.settings = self.load_json(os.path.join("setup", "settings.json"))
        self.theme = self.initialize_theme()

    def load_json(self, filename):
        with open(filename, "r") as f:
            return json.load(f)

    def initialize_theme(self):
        fontdir = os.path.join("data", "fonts")
        return {
            "font": pg.font.Font(os.path.join(fontdir, f"{self.settings["font"]}.ttf"), self.settings["font_size"]),
            "small_font": pg.font.Font(None, 18),
            "background": self.settings["theme"]["background"],
            "tcolor": self.settings["button"]["text"],
            "bcolor": self.settings["button"]["background"],
            "s_bcolor": self.settings["button"]["sbackground"],
            "gap": self.settings["button"]["gap"],
            "shape": self.settings["button"]["shape"]
        }

    def get_layout(self, key):
        return self.layouts.get(key, {})

    def get_setting(self, *keys):
        """By providing a list of argument the function will nest them
        and return the value example key1, key2 -> sett[key1][key2]"""
        value = self.settings
        for key in keys:
            value = value.get(key, {})
        return value

    def get_theme(self, key):
        return self.theme.get(key)

config = ConfigManager()
