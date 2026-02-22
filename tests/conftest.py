import json
import os
import pytest

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

@pytest.fixture(scope="session")
def config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture()
def login_url(config):
    return config["base_url"].rstrip("/") + config["login_path"]