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
from pathlib import Path
from typing import Optional

app = typer.Typer()
state = {
    # container for global variables:
    "datameta_url": None,
    "token": None
}

@app.callback()
def main(config:Optional[Path] = typer.Option(None)):
    pass

if __name__ == "__main__":
    app()
