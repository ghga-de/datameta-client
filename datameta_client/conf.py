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

import yaml
import os
import datameta_client_lib

class ConfigError(RuntimeError):
    pass

def read(path:str = None):
    """Read the runtime configuration either from a specified path or from the
    default path in the users home directory"""
    # If no path is specified by the user, set the default config path
    if not path:
        path = os.path.join(os.path.expanduser("~"), ".dmclient.yaml")
        if not os.path.isfile(path):
            raise ConfigError("Configuration file not found")

    # Try to read the config file
    try:
        with open(path, 'r') as config:
            try:
                data = yaml.safe_load(config)
            except yaml.YAMLError as e:
                raise ConfigError(f"Could not parse configuration file '{path}': {e}")
    except Exception as e:
        raise ConfigError(f"Could not open config file '{path}': {e}")

    # Check for mandatory keys to be present
    mandatory_keys = ['datameta_url', 'api_token']

    for key in mandatory_keys:
        if key not in data:
            raise ConfigError(f"Configuration file '{path}' is missing mandatory key '{key}'")

    return datameta_client_lib.Configuration(
            access_token = data['api_token'],
            host = data['datameta_url'] + '/api/v0'
            )
