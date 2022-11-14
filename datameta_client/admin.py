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

from datameta_client_lib import ApiClient
from datameta_client_lib.api import metadata_api
from datameta_client_lib.model.meta_datum import MetaDatum

from datameta_client_lib import ApiClient, ApiException

import requests

from .config import get_config
from .utils import get_list_or_dict_from
from .printing import info, success, result, error
from .errors import JsonObjectError

app = typer.Typer(help="Administrative endpoints that are not accessible for regular users.")

@app.command()
def post_metadatum(
    metadatum_json, 
    url:Optional[str] = None,
    token:Optional[str] = None,
    quiet:bool = False,
) -> dict:
    """Create a new MetaDatum. This is an administrative endpoint that is not accessible for regular users.
    """
    config = get_config(url, token)

    info("Parsing metadatum", quiet)
    metadatum = get_list_or_dict_from(metadatum_json)

    if isinstance(metadatum, list):
        JsonObjectError(
            "A list of metadata definitions is not allowed here." +
            "Please only specify a single metadatum."
        )

    info("Sending metadatum to server", quiet)

    with ApiClient(config) as api_client:
        api_instance = metadata_api.MetadataApi(api_client)
        try:
            metadatum = MetaDatum(**metadatum)
            api_response = api_instance.create_meta_datum(
                meta_datum=metadatum
            )

            success(
                "Your metadatum creation request was " +
                "successfully passed.",
                quiet
            )
            return result(api_response.to_dict(), quiet)

        except ApiException as e:
            if e.status == requests.codes['bad_request']:
                error("The request was not valid: " + str(e), quiet)
            if e.status == requests.codes['forbidden'] or e.status == requests.codes['unauthorized']:
                error("Access forbidden: " + str(e), quiet)
            else:
                error("An error not related to validation occured: " + str(e), quiet)
            return result(False, quiet)
        


@app.command()
def put_metadatum(
    metadatum_id, 
    metadatum_json,
    url:Optional[str] = None, 
    token:Optional[str] = None,
    quiet:bool = False,
) -> dict:
    """Update a MetaDatum. This is an administrative endpoint that is not accessible for regular users.
    """
    config = get_config(url, token)

    info("Parsing metadatum", quiet)
    metadatum = get_list_or_dict_from(metadatum_json)

    if isinstance(metadatum, list):
        JsonObjectError(
            "A list of metadata is not allowed here." +
            "Please only specify a single metadatum."
        )

    info("Sending metadatum to server", quiet)
    with ApiClient(config) as api_client:
        api_instance = metadata_api.MetadataApi(api_client)
        try:
            api_response = api_instance.update_meta_datum(
                id=metadatum_id,
                meta_datum=MetaDatum(**metadatum)
            )

            success("Metadatum was successfully updated.")
            return result(api_response.to_dict(), quiet)

        except ApiException as e:
            if e.status == requests.codes['bad_request']:
                error("The request was not valid: " + str(e), quiet)
            if e.status == requests.codes['forbidden'] or e.status == requests.codes['unauthorized']:
                error("Access forbidden: " + str(e), quiet)
            else:
                error("An error not related to validation occured: " + str(e), quiet)
            return result(False, quiet)
            
@app.command()
def get_metadata(
    url:Optional[str] = None, 
    token:Optional[str] = None,
    quiet:bool = False,
) -> bool:
    """Get the metadata definitions that are configured for this site.
    """

    config = get_config(url, token)

    with ApiClient(config) as api_client:
        api_instance = metadata_api.MetadataApi(api_client)
        api_response = api_instance.get_meta_data()
        return result(api_response, quiet)
