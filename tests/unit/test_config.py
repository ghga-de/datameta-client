import os
from datameta_client.config import get_config, set_global_config
from datameta_client import api_version

# test fixtures:
url = "http://test.test"
api_url = f"{url}/api/{api_version}"
token = os.getenv("DATAMETA_TOKEN")


def test_config_from_env():
    # set env variables
    os.environ["DATAMETA_URL"] = url
    os.environ["DATAMETA_TOKEN"] = token

    # get config and check if it matches
    # the env vars:
    config = get_config()
    assert config.host == api_url
    assert config.access_token == token


def test_config_from_global_config():
    # set global config
    global_config = {
        "url": url,
        "token": token
    }
    set_global_config(global_config)

    # get config and test if it matches
    # the global config
    config = get_config()
    assert config.host == api_url
    assert config.access_token == token
