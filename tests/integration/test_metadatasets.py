"""Test File related actions.
Please Note: This tests require that the datameta storage
can be accessed at the path specified in
the env variable "DATAMETA_STORAGE_PATH".
"""

import os
from datameta_client import metadatasets
import json

# test fixtures:
metadataset_record_json_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fixtures",
    "test_metadataset_record.json"
)
with open(metadataset_record_json_path, "r") as json_file:
    metadataset_record = json.load(json_file)


def test_add_metadataset():
    metadatasets.add(
        metadata_json=json.dumps(metadataset_record)
    )
