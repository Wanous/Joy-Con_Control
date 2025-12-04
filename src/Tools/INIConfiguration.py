import configparser
import os

class ConfigINIManager:
    """
    Class for managing a single .ini configuration file.
    It loads the file only once and stores the data in memory.
    """

    def __init__(self, path: str):
        self.path = path
        self.config = configparser.ConfigParser()
        self._load()

    def _load(self):
        """Loads the configuration file."""
        if not os.path.exists(self.path):
            return None
        self.config.read(self.path, encoding="utf-8")

    def save(self):
        """Saves the current configuration to the file."""
        with open(self.path, "w", encoding="utf-8") as f:
            self.config.write(f)

    def get(self, section: str, option: str, fallback=None):
        """Retrieves a value from the config."""
        try:
            return self.config.get(section, option, fallback=fallback)
        except Exception:
            return fallback

    def getfloat(self, section: str, option: str, fallback=None):
        """Retrieves a float value."""
        try:
            return self.config.getfloat(section, option, fallback=fallback)
        except Exception:
            return fallback

    def getboolean(self, section: str, option: str, fallback=None):
        """Retrieves a Boolean value."""
        try:
            return self.config.getboolean(section, option, fallback=fallback)
        except Exception:
            return fallback

    def set(self, section: str, option: str, value):
        """Modifies a value"""
        self.config.set(section, option, str(value))

    def sections(self):
        """Returns the list of sections."""
        return self.config.sections()

    def items(self, section: str):
        """Returns the key/value pairs of a section."""
        return dict(self.config.items(section))

    def __getitem__(self, section: str):
        """Allows access to a section like a dictionary."""
        return self.config[section]
    
