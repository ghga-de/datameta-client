import os
from datameta_client import metadatasets
import json

from . import fixtures

def test_stage_metadataset():
    metadatasets.stage(
        metadata_json=json.dumps(fixtures.metadataset_record)
    )
