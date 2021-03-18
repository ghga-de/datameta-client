import os
from datameta_client import submissions, metadatasets, files
from . import fixtures
from .utils import id_in_response

# establish fixtures file and metadataset fixtures in the db:
file_ids = [
    files.stage(path=f["path"])["id"]["uuid"]
    for f in fixtures.files
]


def test_prevalidate_and_submission():
    metadataset_ids = fixtures.get_fresh_metadataset_id()

    valid = submissions.prevalidate(
        metadataset_ids=metadataset_ids,
        file_ids=file_ids,
        label="test"
    )
    assert valid, "Submission failed prevalidation."

    response = submissions.submit(
        metadataset_ids=metadataset_ids,
        file_ids=file_ids,
        label="test"
    )
    assert id_in_response(response, has_site_id=True)
