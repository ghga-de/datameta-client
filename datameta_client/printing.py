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

"""Module containing methods to print to the user"""

import json
from typer import style, echo
from typer.colors import BLUE, GREEN, YELLOW, RED, MAGENTA
from typing import Union, Any
from datetime import datetime
from copy import deepcopy
from datameta_client_lib.model_utils import OpenApiModel


def print_message(message:str, prefix:str, color:str, quiet=False):
    """Base function to be used by the other print functions
    to print to stderr."""
    if not quiet:
        styled_prefix = style(
            f"[{prefix}]: ",
            fg=color,
            bold=True
        )

        styled_message = style(
            message,
            fg=color,
            bold=False
        )

        echo(styled_prefix + styled_message, err=True)


def info(message:str, quiet=False):
    """Print an info of the progress of the action."""
    print_message(message, "info", YELLOW, quiet)


def warning(message:str, quiet=False):
    """Print a warning. This means that there might
    be something the user needs to be aware of,
    however, the action can still be continued."""
    print_message(message, "warning", MAGENTA, quiet)


def success(message:str, quiet=False):
    """Print a message indicating the final success of an action"""
    print_message(message, "success", GREEN, quiet)


def error(message:str, quiet=False):
    """Print an error message."""
    print_message(message, "error", RED, quiet)


def convert_datetimes_to_str_dict(obj:dict):
    """To be used in convert_datetimes_to_str"""
    obj_ = deepcopy(obj)
    for key, value in obj_.items():
        if isinstance(value, dict):
            for key_, value_ in value.items():
                if isinstance(value_, datetime):
                    obj_[key][key_] = value_.isoformat()
        if isinstance(value, datetime):
            obj_[key] = value.isoformat()
    return obj_


def convert_datetimes_to_str(obj:Union[dict, list]):
    """Convert any datetime fields into iso-formatted strings"""
    assert isinstance(obj, (dict, list)), "obj has to be dict or list of dicts"
    if isinstance(obj, list):
        return [convert_datetimes_to_str_dict(item) for item in obj]
    else:
        return convert_datetimes_to_str_dict(obj)


def format_obj_as_str(obj:Any):
    try:
        return json.dumps(obj, indent=4)
    except:
        return str(obj)


def result(
    result_obj:Any,
    quiet:bool=False
) -> Union[dict, list]:
    """Prints response obj procuded using the datameta_client_lib
    to stdout and returns its content."""

    # print results:
    if not quiet:
        styled_prefix = style(
            "[result]:",
            fg=BLUE,
            bold=True
        )
        echo(styled_prefix, err=True)

        formatted_res_obj = (
            convert_datetimes_to_str(result_obj)
            if isinstance(result_obj, (dict, list))
            else result_obj
        )

        styled_result = style(
            format_obj_as_str(formatted_res_obj),
            fg=BLUE
        )
        echo(styled_result, err=False)

    return result_obj
