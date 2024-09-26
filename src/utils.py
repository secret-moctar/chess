import os

from collections import defaultdict

from src.settings import *
from src.button import Button, CompButton, StackButton
from src.config_manager import config
from src.resource_manager import res_manager
from src.blender import SlideTransition


def parse(menu):
    structure = defaultdict(dict)
    for key in menu:
        if key == "imgs":
            for img in menu[key]:
                path = os.path.join("icons", menu[key][img]["path"])
                pos = menu[key][img]["pos"]
                structure["imgs"][img] = {"img": res_manager.get_pres(path), "pos": pos}
                scaleby = [1, 1] if "scaleby" not in menu[key][img] else menu[key][img]["scaleby"]
                structure["imgs"][img]["scaleby"] = scaleby
        if key == "stacks":
            for st in menu[key]:
                pos = menu[key][st]["pos"]
                pos = WIN_WIDTH * pos[0], WIN_HEIGHT * pos[1]
                structure["stacks"][st] = StackButton(pos, config.get_theme("tcolor"), config.get_theme("bcolor"), config.get_theme("s_bcolor"))
                for but_tex in menu[key][st]["buttons"]:
                    button = menu[key][st]["buttons"][but_tex]
                    if button["type"] == "simple":
                        structure["stacks"][st].push(Button(button["id"], but_tex, config.get_theme("font"), config.get_theme("tcolor"), button["bcolor"], button["s_bcolor"], event=button["event"]))
                    elif button["type"] == "complex":
                        structure["stacks"][st].push(CompButton(button["id"], but_tex, config.get_theme("font"), config.get_theme("tcolor"), button["bcolor"], button["s_bcolor"], button["tabs"], button["paths"], event=button["event"]))
    return structure


def log(info, mode="a"):
    with open("./logs/log.txt", mode) as f:
        f.write(info + "\n")
