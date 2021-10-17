from utils.config import Config
from urllib.parse import urlencode


def get_mods():
    mods = Config.load("config.yml")["mode"]
    return ", ".join(mods)


def create_url(url: str, **kwargs) -> str:
    return url + urlencode(kwargs)
