"""Test File related actions.
Please Note: This tests require that the datameta storage
can be accessed at the path specified in
the env variable "DATAMETA_STORAGE_PATH".
"""

import os
from datameta_client import files

# test fixtures:
file_name = "test_file_1.txt"
file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fixtures",
    file_name
)
with open(file_path, "r") as test_file:
    file_content = test_file.read()
storage_path = os.getenv("DATAMETA_STORAGE_PATH")

def test_add_file():
    # remove any files from the datameta storage:
    old_files = os.listdir(storage_path)
    for old_file in old_files:
        os.remove(os.path.join(storage_path, old_file))

    # upload file through API:
    files.add(
        name=file_name,
        path=file_path
    )

    # Check if file appears in storage:
    uploaded_files = os.listdir(storage_path)
    assert len(uploaded_files)==1, (
        "No or too many files appear in the storage path"
    )
    uploaded_file = os.path.join(storage_path, uploaded_files[0])
    with open(uploaded_file, "r") as ufile:
        uploaded_file_content = ufile.read()
    assert uploaded_file_content==file_content, (
        "File contents before and after upload do not match"
    )

