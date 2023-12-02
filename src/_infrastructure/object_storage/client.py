import datetime
from google.cloud import storage
from uuid import uuid4

from _infrastructure.object_storage.configs import CLOUD_STORAGE_BUCKET, CLOUD_STORAGE_CONFIG_FILE


class ObjectStorageClient:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(
            CLOUD_STORAGE_CONFIG_FILE
        )
        self.bucket = self.client.get_bucket(CLOUD_STORAGE_BUCKET)

    def post_presigned_url(self, extension: str) -> tuple[str, str]:
        uuid = uuid4().hex
        file_name = f"{uuid}.{extension}"
        blob = self.bucket.blob(file_name)
        return (
            file_name,
            blob.generate_signed_url(
                version='v4',
                expiration=datetime.timedelta(minutes=1),
                method='POST',
                headers={
                    "x-goog-content-length-range": "0,104857600"
                }
            )
        )

    def delete_file(self, file_name: str):
        blob = self.bucket.blob(file_name)
        blob.delete()
