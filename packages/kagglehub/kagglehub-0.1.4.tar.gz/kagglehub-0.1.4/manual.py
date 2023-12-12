import os

from kagglehub.clients import KaggleApiV1Client


def _upload_blob(file_path):
    print(file_path)
    data = {
        "fileName": os.path.basename(file_path)
    }
    print(data)
    content_length = os.path.getsize(file_path)
    last_modified_epoch_seconds = int(os.path.getmtime(file_path))
    api_client = KaggleApiV1Client()
    response = api_client.post(f"/models/upload/file/{content_length}/{last_modified_epoch_seconds}", data)
    print(response)
    if 'error' in response and response['error'] != "":
        raise BackendError(response['error'])
    
_upload_blob("/usr/local/google/home/rosbo/Documents/dot.png")