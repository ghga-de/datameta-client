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

from typer import style, echo
from typer.colors import BLUE, GREEN, YELLOW, RED 

def print_message(message:str, prefix:str, color:str, quiet=False):
    """Base function to be used by the other print functions"""
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

        echo(styled_prefix + styled_message)


def info(message:str, quiet=False):
    """Print an info of the progress of the action."""
    print_message(message, "info", BLUE, quiet)


def warning(message:str, quiet=False):
    """Print a warning. This means that there might
    be something the user needs to be aware of,
    however, the action can still be continued."""
    print_message(message, "warning", YELLOW, quiet)


def success(message:str, quiet=False):
    """Print a message indicating the final success of an action"""
    print_message(message, "success", GREEN, quiet)
