import os
from datameta_client import metadatasets
import json

from . import fixtures
from .utils import id_in_response

def test_stage_metadataset():
    response = metadatasets.stage(
        metadata_json=json.dumps(fixtures.metadataset_record)
    )
    assert id_in_response(response, has_site_id=True)
