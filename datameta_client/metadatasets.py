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
from typing import Optional, List
from datetime import datetime, timezone

from datameta_client_lib import ApiClient
from datameta_client_lib.api import metadata_api
from datameta_client_lib.model.meta_data_set import MetaDataSet
from datameta_client_lib import ApiClient, ApiException

from .config import get_config
from .utils import get_list_or_dict_from
from .printing import info, success, result

app = typer.Typer()


@app.command()
def stage(
    metadata_json, # dict or str
                   # (Union type not yet supported by typer)
    url:Optional[str] = None,
    token:Optional[str] = None,
    quiet:bool = False,
) -> dict:
    """Stage a single metadataset record.

    The metadata record may be given as a JSON string,
    as a path to a JSON file, or as Python dict
    (the latter is not available when used from the CLI).
    """
    config = get_config(url, token)

    info("Parsing metadata record", quiet)
    metadata_record = get_list_or_dict_from(metadata_json)
    if isinstance(metadata_record, list):
        JsonObjectError(
            "A list of metadata records is not allowed here." +
            "Please only specify a single record."
        )

    info("Sending metadata to server", quiet)
    with ApiClient(config) as api_client:
        api_instance = metadata_api.MetadataApi(api_client)
        meta_data_set = MetaDataSet(record=metadata_record)
        api_response = api_instance.create_meta_data_set(
            meta_data_set=meta_data_set
        )

    success("Metadata record successfully staged.")
    return result(api_response.to_dict(), quiet)

def _add_timezone(dt: Optional[datetime]):
    """Convert to UTC if not None, otherwise return None"""
    if dt:
        return dt.astimezone(timezone.utc)
    return dt

@app.command()
def search(
        submitted_before: Optional[datetime] = None,
        submitted_after: Optional[datetime] = None,
        awaiting_service: Optional[str] = None,
        url:Optional[str] = None,
        token:Optional[str] = None,
        quiet:bool = False
        ) -> List[dict]:
    """Query metadatasets according to search critera. If datetimes are
    specified without a timezone, they are assumed to be local time. Note that
    specifying a timezone is only possible programmatically."""

    config = get_config(url, token)

    # Converting the datetimes to UTC is done only to have any timezone
    # information at all. datetime objects without a timezone will be rejected
    # by the API as invalid ISO strings. In principle they can be submitted in
    # an arbitrary timezone. Applying `astimezone(utc)` to datetime objects
    # without a timezone annotation assumes local time.
    args = {
            'submitted_before': _add_timezone(submitted_before),
            'submitted_after': _add_timezone(submitted_after),
            'awaiting_service': awaiting_service
            }

    args = { k: v for k, v in args.items() if v is not None }

    info("Sending query to server", quiet)
    with ApiClient(config) as api_client:
        api_instance   = metadata_api.MetadataApi(api_client)
        api_response   = api_instance.get_meta_data_sets(**args)

    res = [elem.to_dict() for elem in api_response]
    return result(res, quiet)
