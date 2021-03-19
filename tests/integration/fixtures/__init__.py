import os
import json
from random import choice
from string import ascii_letters, digits
from copy import deepcopy


base_dir = os.path.dirname(os.path.abspath(__file__))

# metadataset fixtures:
metadataset_record_json_path = os.path.join(
    base_dir,
    "test_metadataset_record.json"
)
with open(metadataset_record_json_path, "r") as json_file:
    metadataset_record = json.load(json_file)

# change #ID to not fail global uniqueness constraint:
#! to be removed:
def replace_ID(mset):   
    mset_ = deepcopy(mset)
    mset_["#ID"] = (
        "".join(choice(ascii_letters).upper() for _ in range(2)) +
        "".join(str(choice(digits)) for _ in range(2))
    )
    return mset_

from datameta_client import metadatasets
def get_fresh_metadataset_id(): 
    mset = replace_ID(metadataset_record)
    return [
        metadatasets.stage(
            metadata_json=mset
        )["id"]["uuid"]
    ]
#! to be removed end

# file fixtures:
storage_path = os.getenv("DATAMETA_STORAGE_PATH")

def get_content(path:str):
    with open(path, "r") as test_file:
        return test_file.read()

files = [
    {
        "name": name,
        "path": os.path.join(base_dir, name),
        "content": get_content(os.path.join(base_dir, name))
    }
    for name in os.listdir(base_dir)
    if "test_file_" in name
]
