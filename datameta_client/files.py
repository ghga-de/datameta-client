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

import os
import typer
import hashlib
import json
import requests
from typing import Optional

from datameta_client_lib import ApiClient
from datameta_client_lib.api import files_api, remote_procedure_calls_api
from datameta_client_lib.model.file_announcement import FileAnnouncement
from datameta_client_lib.model.file_upload_response import FileUploadResponse
from datameta_client_lib.model.file_update_request import FileUpdateRequest

from .config import get_config
from .printing import info, success, result

app = typer.Typer()

@app.command()
def stage(
    path: str,
    name:Optional[str]    = None,
    url:Optional[str]     = None,
    token:Optional[str]   = None,
    quiet:bool            = False,
) -> dict:
    """Stage and upload a single file.

    Please specify the path to the file and,
    optionally, a file name that is used for
    storing the file (by default the original file
    name will be used).
    """
    config = get_config()

    # Compute the checksum of the provided file
    with open(path, 'rb') as infile:
        md5 = hashlib.md5(infile.read()).hexdigest()

    # if name not provided, infer it from the file
    name = os.path.basename(path)

    # [API CALL 1]
    # Announce the file to the API. The announcement provides the filename and
    # the checksum of the file data.
    with ApiClient(config) as api_client:
        api_instance = files_api.FilesApi(api_client)
        file_announcement = FileAnnouncement(
            name=name,
            checksum=md5,
        )
        info("Announcing file", quiet)
        api_response_announce = api_instance.create_file(file_announcement=file_announcement)

    # [API CALL 2][NOT PART OF THE REST API]
    # Make a multipart/form-data POST upload to the location received in the
    # announcement response
    info("Uploading data...", quiet)
    with open(path, 'rb') as infile:
        api_response_upload = requests.post(
                api_response_announce['url_to_upload'],
                headers=api_response_announce.request_headers,
                files = { 'file' : infile } )
        api_response_upload.raise_for_status()
    info("Upload completed", quiet)

    # [API CALL 3]
    info("Informing the backend that the file upload was performed", quiet)
    with ApiClient(config) as api_client:
        api_instance = files_api.FilesApi(api_client)
        # Use the file ID as received in the announcement response
        id = api_response_announce['id']['uuid']

        file_update_request = FileUpdateRequest(
            content_uploaded=True,
        )
        api_response = api_instance.update_file(id, file_update_request=file_update_request)

    success(f"File \"{name}\" was successfully added.", quiet)
    return result(api_response.to_dict(), quiet)

@app.command()
def download_url(
        file_id: str,
        expires: Optional[int]   = 1,
        url:Optional[str]        = None,
        token:Optional[str]      = None,
        quiet:bool               = False
        ) -> dict:

    """Obtain a download URL for a given file ID.

    Please specify the file ID (UUID or site ID) and a desired expiration time
    of the download URL in minutes."""
    config = get_config()

    info(f"Requesting download URL for file {file_id}", quiet)
    with ApiClient(config) as api_client:
        # Create an instance of the API class
        api_instance = remote_procedure_calls_api.RemoteProcedureCallsApi(api_client)

        api_response = api_instance.get_file_url(file_id, expires=expires)

    success("Download URL received.", quiet)
    return result(api_response.to_dict(), quiet)
