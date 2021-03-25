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
from typing import Optional, List

from .config import get_config
from .utils import get_list_or_dict_from
from .printing import info, success, result, error
from . import metadatasets, files, submissions

app = typer.Typer()


@app.command()
def stage_and_submit(
    metadatasets_json, # a single or a list of records dicts,
                       # or the equivalent in a json string or file
    files_dir:Optional[str],
    label:Optional[str] = None,
    url:Optional[str] = None, 
    token:Optional[str] = None,
    quiet:bool = False,
) -> dict:
    """This "shortcut" will stage and submit files and metadata records in one go.

    It requires one or multiple metadata records and the path to the directory
    containing the files to upload. The metadata records may be given as a JSON string,
    as a path to a JSON file, or as Python (list of) dict (the latter is not available when
    used from the CLI).

    Optionally, you may also provide a human-readable label for the submission.
    """
    info(
        "This will stage and directly submit metadatasets and files in a single run.",
        quiet
    )

    # parse metadatasets_json:
    info("Parsing metadata", quiet)
    msets = get_list_or_dict_from(metadatasets_json)
    msets = msets if isinstance(msets, list) else [msets]

    # get a flat set of record values in that metadataset:
    record_values = set()
    for record in msets:
        record_values.update(
            {val for val in record.values()}
        )

    # list files in files_dir and find those 
    # that were mentioned in the metadatasets:
    info("Searching for files to upload from the files_dir", quiet)
    files_to_upload = {
        os.path.join(files_dir, file_)
        for file_ in os.listdir(files_dir)
        if file_ in record_values
    }

    # stage metadatasets:
    info("Staging metadatasets ...", quiet)
    msets_uploaded = []
    for idx, mset in enumerate(msets):
        info(f"Staging metadataset {idx+1} of {len(msets)}")
        msets_uploaded.append(
            metadatasets.stage(
                mset,
                url=url,
                token=token,
                quiet=True
            )
        )
    success("All metadatasets successfully staged.", quiet)
    _ = result(msets_uploaded, quiet)
    
    # stage files:
    info("Staging files ...", quiet)
    files_uploaded = []
    for idx, file_ in enumerate(files_to_upload):
        info(f"Staging file {idx+1} of {len(files_to_upload)}")
        files_uploaded.append(
            files.stage(
                file_,
                url=url,
                token=token,
                quiet=True
            )
        )
    success("All files successfully staged.", quiet)
    _ = result(files_uploaded, quiet)

    # submit all staged files and metadatasets:
    info("Submitting the staged files and metadatasets.")
    mset_ids = [mset["id"]["uuid"] for mset in msets_uploaded]
    file_ids = [file_["id"]["uuid"] for file_ in files_uploaded]
    submission_result = submissions.submit(
        metadataset_ids=mset_ids,
        file_ids=file_ids,
        label=label,
        url=url,
        token=token,
        quiet=True
    )
    success("Successfully completed submission.", quiet)
    return result(submission_result, quiet)
