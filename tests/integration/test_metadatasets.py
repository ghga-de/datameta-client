"""Test File related actions.
Please Note: This tests require that the datameta storage
can be accessed at the path specified in
the env variable "DATAMETA_STORAGE_PATH".
"""

import os
from datameta_client import metadatasets
import json

from . import fixtures

def test_add_metadataset():
    metadatasets.add(
        metadata_json=json.dumps(fixtures.metadataset_record)
    )
