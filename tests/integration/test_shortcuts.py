from datameta_client import shortcuts
from . import fixtures
from .utils import id_in_response

def test_prevalidate_and_submission():
    metadataset_record = fixtures.replace_ID(fixtures.metadataset_record)

    response = shortcuts.stage_and_submit(
        metadatasets_json=metadataset_record,
        files_dir=fixtures.base_dir,
        label="test"
    )
    assert id_in_response(response, has_site_id=True)