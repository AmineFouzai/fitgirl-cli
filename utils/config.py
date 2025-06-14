import configparser
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "./config/config.ini")


def get_config_value(section: str, key: str, fallback: str) -> str:
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        return config.get(section, key)
    except Exception:
        return fallback
