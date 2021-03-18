import os
from datameta_client import files
from . import fixtures
from .utils import id_in_response

def test_stage_file():
    # upload file through API:
    response = files.stage(
        name=fixtures.files[0]["name"],
        path=fixtures.files[0]["path"]
    )
    assert id_in_response(response, has_site_id=True)
