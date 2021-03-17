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

import sys
import typer
import json
import hashlib
import requests
from pprint import pprint
from typing import Optional

from datameta_client_lib import ApiClient, ApiException
from datameta_client_lib.api import files_api, metadata_api
from datameta_client_lib.model.meta_data_set import MetaDataSet
from datameta_client_lib.model.file_announcement import FileAnnouncement
from datameta_client_lib.model.file_upload_response import FileUploadResponse
from datameta_client_lib.model.file_update_request import FileUpdateRequest

from .config import get_config
from .utils import get_dict_from
from .printing import info, success

app = typer.Typer()


@app.command()
def add(
    metadata_json, # dict or str 
                   # (Union type not yet supported by typer)
    url:Optional[str] = None, 
    token:Optional[str] = None,
    quiet:bool = False,
):
    config = get_config(url, token)
    
    info("Parsing metadata record", quiet)
    metadata_record = get_dict_from(metadata_json)

    with ApiClient(config) as api_client:
        api_instance = metadata_api.MetadataApi(api_client)
        meta_data_set = MetaDataSet(record=metadata_record)
        info("Sending metadata to server", quiet)
        api_response = api_instance.create_meta_data_set(
            meta_data_set=meta_data_set
        )
        
    success("Metadata record successfully added.")
    
