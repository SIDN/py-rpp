import yaml
from pathlib import Path
import pytest

@pytest.fixture
def get_credentials():
    config_path = Path(__file__).parent / "config.test.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    username = config["auth"]["username"]
    password = config["auth"]["password"]
    return (username, password)