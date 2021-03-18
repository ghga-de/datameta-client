import os
import tempfile
import json
from datameta_client import utils

# test fixtures:
test_dict = {
    "test": "test"
}

def test_get_config():
    # write test_dict to json file:
    _, tmp_json = tempfile.mkstemp()
    with open(tmp_json, "w") as tfile:
        json.dump(test_dict, tfile)
    
    # create a list of equivalent objects,
    # containing:
    # - the original dict
    # - a json string representation
    # - the path to a file containing a json representation
    test_objs = [
        test_dict,
        json.dumps(test_dict),
        tmp_json        
    ]

    # utils.get json should always return
    # the original dict:
    for obj in test_objs:
        assert utils.get_list_or_dict_from(obj) == test_dict
