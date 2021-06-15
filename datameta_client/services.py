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
from copy import deepcopy
from typing import Optional

from datameta_client_lib import ApiClient
from datameta_client_lib.api import services_api
from datameta_client_lib.model.service_execution import ServiceExecution

from .config import get_config
from .utils import get_list_or_dict_from, list_or_comma_sep_str
from .printing import info, success, result

app = typer.Typer()

@app.command('list')
def list_(
    url:Optional[str] = None,
    token:Optional[str] = None,
    quiet:bool = False,
) -> dict:
    """List services.
    """

    config = get_config(url, token)

    info("Querying configured services.", quiet)

    with ApiClient(config) as api_client:
        api_instance = services_api.ServicesApi(api_client)
        api_response = api_instance.get_service_info()
    success("Retrieved configured services.", quiet)

    res = result(api_response, quiet)

    return res

@app.command()
def execute(
        service_id: str,
        metadataset_id: str,
        metadata_json,
        file_ids,  # list of string or commaseperated string
        url:Optional[str]     = None,
        token:Optional[str]   = None,
        quiet:bool            = False
        ) -> dict:
    """Report the result of a service execution.

    The service and metadataset IDs can be site IDs or UUIDs. The metadataset
    JSON argument holds the key / value pairs for the records holding the
    service execution result. When using this function programmatically, python
    dictionaries and JSON strings can be used interchangeably. If the service
    resports for a file metadatum, the corresponding files have to be uploaded
    beforehand and the IDs have to be specified as file_ids. Provide an empty
    string / list to include no files."""

    config = get_config(url, token)


    file_ids = list_or_comma_sep_str(file_ids) if file_ids else []

    info("Parsing provided metadata records", quiet)
    metadata_record = get_list_or_dict_from(metadata_json)
    if isinstance(metadata_record, list):
        JsonObjectError(
            "A list of metadata records is not allowed here." +
            "Please only specify a single record."
        )

    info("Sending service execution to server", quiet)

    with ApiClient(config) as api_client:
        api_instance = services_api.ServicesApi(api_client)
        service_execution = ServiceExecution(
                record=metadata_record,
                file_ids=file_ids
                )
        api_response = api_instance.service_set_meta_datum(service_id, metadataset_id, service_execution=service_execution)

    success("Successfully reported service execution.", quiet)

    return result(api_response, quiet)
