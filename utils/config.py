from typing import Any

import yaml


class Config:
    def __init__(self, filename: str, mode: str) -> None:
        self.filename = filename
        self._data = self.load(filename=filename)
        self.data = self._data["mode"][mode]

    @staticmethod
    def load(filename: str) -> dict:
        with open(filename, encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
        return data

    def get(self, name: str, default: Any = None) -> Any:
        return self.data.get(name, default)

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name, None)

    def __getitem__(self, name: str) -> Any:
        return self.data.get(name, None)
