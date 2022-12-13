from datameta_client import admin
import json
import string
import random

from . import fixtures
from .utils import id_in_response


def test_get_metadata():
    response = admin.get_metadata()
    default_metadata_names = []
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
    
    get_response = admin.get_metadata()
    
    for metadatum in get_response:
        if metadatum.name == fixtures.metadatum['name']:
            test_uuid = metadatum.id.uuid
    
    fixtures.metadatum['name'] = ''.join(random.choices(string.ascii_uppercase, k=10))

    admin.put_metadatum(
        metadatum_id=test_uuid,
        metadatum_json=json.dumps(fixtures.metadatum)
    )
    
    get_after_put_response = admin.get_metadata()
    for metadatum in get_after_put_response:
        if metadatum.id.uuid == test_uuid:
            assert metadatum.name == fixtures.metadatum['name']

#
#
#

def test_get_appsettings():
    response = admin.get_appsettings()
    for setting in response:
        if setting["key"] == "subject_welcome_token":
            assert setting["value"] == 'Your registration was confirmed!'

def test_put_appsettings():
    response = admin.get_appsettings()
    for setting in response:
        if setting["key"] == "subject_forgot_token":
            response_put = admin.put_appsettings(
                appsetting_id=setting["id"]["uuid"],
                appsetting_json={"value": "TEST"}
                )
            assert response_put is None
    
    response = admin.get_appsettings()
    for setting in response:
        if setting["key"] == "subject_forgot_token":
            assert setting["value"] == 'TEST'
    