import os
from datameta_client import files
from . import fixtures


def test_stage_file():
    # remove any files from the datameta storage:
    old_files = os.listdir(fixtures.storage_path)
    for old_file in old_files:
        os.remove(os.path.join(fixtures.storage_path, old_file))

    # upload file through API:
    files.stage(
        name=fixtures.files[0]["name"],
        path=fixtures.files[0]["path"]
    )

    # Check if file appears in storage:
    uploaded_files = os.listdir(fixtures.storage_path)
    assert len(uploaded_files)==1, (
        "No or too many files appear in the storage path"
    )
    uploaded_file = os.path.join(fixtures.storage_path, uploaded_files[0])
    with open(uploaded_file, "r") as ufile:
        uploaded_file_content = ufile.read()
    assert uploaded_file_content==fixtures.files[0]["content"], (
        "File contents before and after upload do not match"
    )

