import os
from datameta_client import metadatasets
import json

from . import fixtures

def test_add_metadataset():
    metadatasets.add(
        metadata_json=json.dumps(fixtures.metadataset_record)
    )
