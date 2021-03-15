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
from pathlib import Path
from typing import Optional
from . import conf
from datameta_client_lib import ApiClient, ApiException
from datameta_client_lib.api import files_api, metadata_api
from datameta_client_lib.model.meta_data_set import MetaDataSet
from datameta_client_lib.model.file_announcement import FileAnnouncement
from datameta_client_lib.model.file_upload_response import FileUploadResponse
from datameta_client_lib.model.file_update_request import FileUpdateRequest

app = typer.Typer()
app_config = None

@app.command()
def addfile(name:str, path: str):
    # Compute the checksum of the provided file
    with open(path, 'rb') as infile:
        md5 = hashlib.md5(infile.read()).hexdigest()

    # [API CALL 1]
    # Announce the file to the API. The announcement provides the filename and
    # the checksum of the file data.
    with ApiClient(app_config) as api_client:
        api_instance = files_api.FilesApi(api_client)
        file_announcement = FileAnnouncement(
            name=name,
            checksum=md5,
        )
        print("Announcing file")
        try:
            api_response_announce = api_instance.create_file(file_announcement=file_announcement)
        except ApiException as e:
            print("Exception when calling FilesApi->create_file: %s\n" % e)
            sys.exit(1)

    # [API CALL 2][NOT PART OF THE REST API]
    # Make a multipart/form-data POST upload to the location received in the
    # announcement response
    print("Uploading data...", end = "")
    with open(path, 'rb') as infile:
        api_response_upload = requests.post(
                api_response_announce['url_to_upload'],
                # [!!] TODO THIS IS TO BE REMOVED!
                headers={'Authorization' : 'Bearer ' + app_config.access_token, **api_response_announce.request_headers },
                files = { 'file' : infile } )
        try:
            api_response_upload.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("\nThe file upload failed.\n")
            pprint(err)
            sys.exit(1)
    print(" Done.")

    # [API CALL 3]
    # Inform the backend that the file was uploaded
    print("Informing the backend that the file upload was performed...", end="")
    with ApiClient(app_config) as api_client:
        api_instance = files_api.FilesApi(api_client)
        # Use the file ID as received in the announcement response
        id = api_response_announce['id']['uuid']

        file_update_request = FileUpdateRequest(
            content_uploaded=True,
        )
        try:
            api_response = api_instance.update_file(id, file_update_request=file_update_request)
            print(" Done.")
        except ApiException as e:
            if e.status == requests.codes['bad_request']:
                print("\nThe file update failed: The request was malformed.")
            elif e.status == requests.codes['not_found']:
                print("\nThe file update failed: The upload URL is invalid")
            elif e.status == requests.codes['forbidden']:
                print("\nThe file update failed: Forbidden")
            elif e.status == requests.codes['conflict']:
                print("\nThe file update failed: Checksum mismatch")
            sys.exit(1)

@app.command()
def addmeta(metadata: str):
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

@app.callback()
def main(config:Optional[Path] = typer.Option(None)):
    global app_config
    try:
        app_config = conf.read(config)
    except conf.ConfigError as e:
        print(e)
        sys.exit(1)
    pass

if __name__ == "__main__":
    app()
