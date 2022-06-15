import os
import toml
import logging

from appdirs import AppDirs
import dialite

dirs = AppDirs("AppleMusicRP", "wxllow")

if not os.path.exists(dirs.user_data_dir):
    os.makedirs(dirs.user_data_dir, exist_ok=True)


class Config:
    def __init__(self) -> None:
        self._loc = os.path.join(dirs.user_data_dir, "config.toml")

        if not os.path.exists(self._loc):
            with open(self._loc, "w") as f:
                pass

        try:
            self._config = toml.load(self._loc)
        except Exception as e:
            logging.error("Config file corrupt, resetting config.")
            self._config = {}
            self.save()

    @property
    def config(self):
        return self._config

    def save(self):
        with open(self._loc, "w") as f:
            toml.dump(self._config, f)
