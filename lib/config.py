import os
import sys

from qtawesome.iconic_font import json


class ConfigManager:
    def __init__(self):
        self.app_name = "veia"
        self.conf_dir = self._get_config_directory()
        self.conf_file = self._get_config_file()
        self.config = {}

        self.load_config()

    def _get_config_directory(self):
        if sys.platform == "linux":
            config_dir = os.path.join(os.path.expanduser("~"), ".config", self.app_name)
        else:
            config_dir = os.path.join(os.path.expanduser("~"), f".{self.app_name}")
        os.makedirs(config_dir, exist_ok=True)
        return config_dir

    def _get_config_file(self):
        file = os.path.join(self.conf_dir, "config.json")
        return file

    def load_config(self):
        if not os.path.exists(self.conf_file):
            with open(self.conf_file, "w") as f:
                f.write("{}")

        try:
            with open(self.conf_file, "r") as f:
                data = json.load(f)
                self.config = data
        except Exception as e:
            print(f"Error loading config: {e}")

    def save_config(self):
        if self.config:
            with open(self.conf_file, "w") as f:
                json.dump(self.config, f, indent=4)

    def get(self, section, key, default=""):
        return self.config.get(section, {}).get(key, default)

    def set(self, section, key, value):
        if not self.config.get(section):
            self.config[section] = {}
        self.config[section][key] = value
        self.save_config()
