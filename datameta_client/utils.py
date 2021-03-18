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
import json
from typing import Union, List

from .errors import JsonObjectError

JSON=Union[dict, str, list]

def get_list_or_dict_from(obj:JSON) -> dict:
    """Accepts a dict or a str which can either be a json representation
    or the path to a json file. The function tries parse the information
    and return a dict."""
    # if obj is a dict or a list, directly return:
    if isinstance(obj, dict) or isinstance(obj, list):
        return obj

    if isinstance(obj, str):
        try:
            # if obj maps to a file:
            if os.path.isfile(obj):
                with open(obj, "r") as json_file:
                    return json.load(json_file)
        except Exception as e:
            raise JsonObjectError(
                "The provided file could not be parsed: " + str(e)
            )

        try:
            # try to parse string as json:
            return json.loads(obj)
        except:
            raise JsonObjectError(
                "The provided string did neither map to a json file " +
                "nor could it be parsed as json."
            )
    
    raise TypeError(
        "Please either provide a dict or a string which either can be " +
        "parsed as json or points to a json file."
    )


def list_or_comma_sep_str(obj:Union[str, List[str]]):
    # if its a list of string, return
    if isinstance(obj, list):
        return obj
    # if its a single string, break it down by commas:
    elif isinstance(obj, str):
        return [item.strip() for item in obj.split(',')]
    else:
        raise ValueError(
            "Please either provide a list of strings or " +
            "a single strings with items seperated by commas.")
