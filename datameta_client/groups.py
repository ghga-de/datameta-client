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
from typing import Optional
from .config import get_config
from .printing import result
from datameta_client_lib import ApiClient
from datameta_client_lib.api import groups_api
from datameta_client_lib.model.group_response import GroupResponse
from datameta_client_lib.model.error_model import ErrorModel

app = typer.Typer()

@app.command()
def get_group(
    id: str,
    url:Optional[str]     = None,
    token:Optional[str]   = None,
    quiet:bool            = False,
) -> dict:

    config = get_config()

    with ApiClient(config) as api_client:
        # Create an instance of the API class
        api_instance = groups_api.GroupsApi(api_client)

        # Get group information
        api_response = api_instance.group_information_request(id)
        return result(api_response.to_dict(), quiet)
