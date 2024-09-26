import os
from functools import lru_cache

from src.settings import *

class ResourceManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.resources = {}
        self.resource_paths = {}

    def register(self, name, rel_path):
        """ Register a resource with a name and it's relative path."""
        full_path = os.path.join(self.base_path, rel_path)
        self.resource_paths[name] = full_path

    @lru_cache
    def _load_image(self, path):
        """Internal method, for loading an image. Cache for Efficiency"""
        return pg.image.load(path).convert_alpha()

    @lru_cache
    def _load_sound(self, path):
        """Internal method, for loading a sound. Cache for Efficiency"""
        return pg.mixer.Sound(path)

    def get_resource(self, name):
        """Get a resource by its registered name. Lazy-loads if not
        already loaded."""
        if name in self.resources: return self.resources[name]
        if name not in self.resource_paths:
            raise KeyError(f"Resource {name} not registered.")

        path = self.resource_paths[name]
        extension = os.path.splitext(path)[-1].lower()

        if extension in {".png", ".jpg", ".bmp", ".gif", ".svg"}:
            self.resources[name] = self._load_image(path)
        elif extension in {".mp3", ".wav", ".ogg"}:
            self.resources[name] = self._load_sound(path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return self.resources[name]

    def get_pres(self, path):
        """Get a resource by its full path. Lazy-loads if not already loaded."""
        path = os.path.join(self.base_path, path)
        if path in self.resources: return self.resources[path]

        extension = os.path.splitext(path)[1].lower()
        if extension in ['.png', '.jpg', '.bmp', '.gif']:
            self.resources[path] = self._load_image(path)
        elif extension in ['.wav', '.ogg', '.mp3']:
            self.resources[path] = self._load_sound(path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return self.resources[path]

    def preload_resources(self):
        """Preload all registered resources."""
        for name in self.resource_paths:
            self.get_resource(name)

    def unload_resource(self, name):
        """Unload a specific resource to free up memory."""
        if name in self.resources:
            del self.resources[name]

    def clear_cache(self):
        """Clear the entire resource cache."""
        self.resources.clear()
        self._load_image.cache_clear()
        self._load_sound.cache_clear()

res_manager = ResourceManager("data")  # resource manager

# load some resources
p_chess = "chess-pieces"
p_join = os.path.join
res_manager.register("K", p_join(p_chess, "Chess_klt60.png"))
res_manager.register("k", p_join(p_chess, "Chess_kdt60.png"))
res_manager.register("Q", p_join(p_chess, "Chess_qlt60.png"))
res_manager.register("q", p_join(p_chess, "Chess_qdt60.png"))
res_manager.register("B", p_join(p_chess, "Chess_blt60.png"))
res_manager.register("b", p_join(p_chess, "Chess_bdt60.png"))
res_manager.register("R", p_join(p_chess, "Chess_rlt60.png"))
res_manager.register("r", p_join(p_chess, "Chess_rdt60.png"))
res_manager.register("N", p_join(p_chess, "Chess_nlt60.png"))
res_manager.register("n", p_join(p_chess, "Chess_ndt60.png"))
res_manager.register("P", p_join(p_chess, "Chess_plt60.png"))
res_manager.register("p", p_join(p_chess, "Chess_pdt60.png"))

# load some image for marking
res_manager.register("blue_circle", p_join("icons", "icons8-circle-30.png"))
res_manager.register("red_circle", p_join("icons", "icons8-circle-48.png"))
res_manager.register("chess_title", p_join("icons", "chess_title.png"))

# register some sound
res_manager.register("button", p_join("sounds", "button_click.mp3"))
res_manager.register("move", p_join("sounds", "move-self.mp3"))
res_manager.register("capture", p_join("sounds", "capture.mp3"))
res_manager.register("check", p_join("sounds", "move-check.mp3"))
res_manager.register("promote", p_join("sounds", "promote.mp3"))
res_manager.register("check_mate", p_join("sounds", "notify.mp3"))
res_manager.register("clock", p_join("sounds", "the-sound-of-the-clock-near-the-chess.mp3"))