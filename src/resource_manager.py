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
