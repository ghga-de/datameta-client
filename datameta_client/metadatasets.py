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

app = typer.Typer()


@app.command()
def add(
    metadata: str,
    url:Optional[str] = None, 
    token:Optional[str] = None,
):
    config = get_config(url, token)

    with ApiClient(app_config) as api_client:
        api_instance = metadata_api.MetadataApi(api_client)
        meta_data_set = MetaDataSet(record=json.loads(metadata))
        try:
            api_response = api_instance.create_meta_data_set(meta_data_set=meta_data_set)
            pprint(api_response)
            print("\nMetadataset successfully uploaded")
        except ApiException as e:
            pprint(json.loads(e.body))
            print("\nMetadataset uploaded failed")
            sys.exit(1)
