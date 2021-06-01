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

import typer
import yaml
from typing import Optional

from .files import app as files_app
from .metadatasets import app as metadatasets_app
from .submissions import app as submissions_app
from .shortcuts import app as shortcuts_app
from .services import app as services_app
from .config import set_global_config


app = typer.Typer()
app.add_typer(files_app, name="files")
app.add_typer(metadatasets_app, name="metadatasets")
app.add_typer(submissions_app, name="submissions")
app.add_typer(shortcuts_app, name="shortcuts")
app.add_typer(services_app, name="services")

@app.callback()
def main(config:str = typer.Option(None)):
    """This is a client to stage and submit files and metadata
    to a datameta server.
    """
    if config:
        with open(config, "r") as cfile:
            set_global_config(yaml.safe_load(cfile))
        

if __name__ == "__main__":
    app()
