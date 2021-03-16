# Copyright 2021 Universität Tübingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import yaml
from pathlib import Path
from typing import Optional
import datameta_client_lib

from . import api_version
from .errors import ConfigError

global_config = { 
    # global default config parameters
    # e.g. set by the CLI when prociding a config file
    "url": None,
    "token": None
}


def set_global_config(config:dict):
    """Sets the global config."""
    global global_config
    global_config=config


def get_config_param(
    name:str,
    config_from_file:dict = {}
):
    """Get config param value and prioritize between different sources.
    See `get_config` for further info"""
    # get value from env variable
    param_from_env = os.getenv(f"DATAMETA_{name.upper()}")
    if param_from_env:
        return param_from_env
    
    # get param value from config file:
    if name in config_from_file and config_from_file[name]:
        return config_from_file[name]

    # get param from global config:
    if name in global_config and global_config[name]:
        return global_config[name]
    
    raise ConfigError(
        f"Parameter {name} not specified. " +
        f"E.g. set using the env variabe " +
        f"\"DATAMETA_{name.upper()}\"."
    )


def get_config(
    url:Optional[str] = None,
    token:Optional[str] = None, 
    config_file:Optional[Path] = None,
):
    """Generate configuration class used by datameta_client_lib.
    Configuration parameters can be supplied by (highest priority first):
        - the function parameters url and token
        - env variables (DATAMETA_URL, DATAMETA_TOKEN)
        - config YAML file provided by "config_file"
        - the global variable "global_config" set by the CLI

    Args:
        url (Optional[str], optional): URL to the datameta instance. Defaults to None.
        token (Optional[str], optional): Token obtained from the datameta instance. Defaults to None.
        config_file (Optional[Path], optional): Path to a config file. Defaults to None.
    """
    # read config file, if provided:
    config_from_file = {}
    if config_file:
        with open(config_file, "r") as cfile:
            config_from_file = yaml.safe_load(config_file)

    # prioritize param info from different sources:
    url = url if url else get_config_param("url", config_from_file)
    token = token if token else get_config_param("token", config_from_file)

    # return configuration for datameta_client_lib
    return datameta_client_lib.Configuration(
        access_token = token,
        host = f"{url}/api/{api_version}"
    )