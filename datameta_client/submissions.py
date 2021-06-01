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
import requests

from datameta_client_lib import ApiClient, ApiException
from datameta_client_lib.api import submissions_api
from datameta_client_lib.model.submission_request import SubmissionRequest

from .config import get_config
from .utils import get_list_or_dict_from, list_or_comma_sep_str
from .printing import info, success, result, error

app = typer.Typer()


@app.command()
def prevalidate(
    metadataset_ids, # list of string or
                     # commaseperated string
    file_ids, # list of string or
                     # commaseperated string
    label:Optional[str] = None,
    url:Optional[str] = None, 
    token:Optional[str] = None,
    quiet:bool = False,
) -> bool:
    """\"Dry-run\" option to check the validity of a submission request. The submission will not
    be stored on the server.

    This requires a list of metadataset IDs and a list of file IDs. The IDs can be either
    given as a comman-separated string or as a Python list of string (the latter is not
    available when using the CLI).

    Optionally, you may also provide a human-readable label for the submission.
    """
    info(
        "This will only validate the request. No submission will be posted.",
        quiet
    )
    config = get_config(url, token)

    metadataset_ids = list_or_comma_sep_str(metadataset_ids)
    file_ids = list_or_comma_sep_str(file_ids)
    
    info("Assembling submission request", quiet)
    submission_request = SubmissionRequest(
        metadataset_ids=metadataset_ids,
        file_ids=file_ids,
        label=label
    )

    info("Sending request for validation", quiet)
    with ApiClient(config) as api_client:
        api_instance = submissions_api.SubmissionsApi(api_client)

        try:
            api_response = api_instance.prevalidate_submission(
                submission_request=submission_request
            )
            success(
                "The pre-validatio of your submission request was " +
                "successfully passed. Feel free to actually post this submission.",
                quiet
            )
            return result(True, quiet)


        except ApiException as e:
            if e.status == requests.codes['bad_request']:
                error("The request was not valid: " + str(e), quiet)
            else:
                error(
                    "An error not related to validation occured: " + str(e),
                    quiet
                )
            return result(False, quiet)


@app.command()
def submit(
    metadataset_ids, # list of string or
                     # commaseperated string
    file_ids, # list of string or
                     # commaseperated string
    label:Optional[str] = None,
    url:Optional[str] = None, 
    token:Optional[str] = None,
    quiet:bool = False,
) -> dict:
    """Submit a set of metadatasets and a set of files.

    This requires a list of metadataset IDs and a list of file IDs. The IDs can be either
    given as a comma-separated string or as a Python list of string (the latter is not
    available when using the CLI).

    Optionally, you may also provide a human-readable label for the submission.
    """
    config = get_config(url, token)
    
    metadataset_ids = list_or_comma_sep_str(metadataset_ids)
    file_ids = list_or_comma_sep_str(file_ids)
    
    info("Assembling submission request", quiet)
    submission_request = SubmissionRequest(
        metadataset_ids=metadataset_ids,
        file_ids=file_ids,
        label=label
    )

    info("Posting submission to the server", quiet)
    with ApiClient(config) as api_client:
        api_instance = submissions_api.SubmissionsApi(api_client)
        api_response = api_instance.create_submission(
            submission_request=submission_request
        )

    success("Submission was successfully posted.")
    return result(api_response.to_dict())
