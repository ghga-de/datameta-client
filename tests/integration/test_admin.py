from datameta_client import admin
import json
import string
import random

from . import fixtures
from .utils import id_in_response

# workaround to access the list of MetaDatumResponse
def list_metadata(response):
    return(response._data_store['value'])

def test_get_metadata():
    response = list_metadata(admin.get_metadata())
    default_metadata_names = ['Date', '#ID', 'ZIP Code', 'FileR1', 'FileR2']
    names = [metadatum.name for metadatum in response]
    for default_metadata_name in default_metadata_names:
        assert default_metadata_name in names

def test_post_metadatum():
    response = admin.post_metadatum(
        metadatum_json=json.dumps(fixtures.metadatum)
    )
    assert id_in_response(response, has_site_id=False)


def test_put_metadatum():
    admin.post_metadatum(
        metadatum_json=json.dumps(fixtures.metadatum)
    )
    
    get_response = list_metadata(admin.get_metadata())
    
    for metadatum in get_response:
        if metadatum.name == fixtures.metadatum['name']:
            test_uuid = metadatum.id.uuid
    
    fixtures.metadatum['name'] = ''.join(random.choices(string.ascii_uppercase, k=10))

    admin.put_metadatum(
        metadatum_id=test_uuid,
        metadatum_json=json.dumps(fixtures.metadatum)
    )
    
    get_after_put_response = list_metadata(admin.get_metadata())
    for metadatum in get_after_put_response:
        if metadatum.id.uuid == test_uuid:
            assert metadatum.name == fixtures.metadatum['name']
