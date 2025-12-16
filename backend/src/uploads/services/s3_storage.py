import json
from io import BytesIO

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error

from src.uploads.services.storage import StorageInterface


class S3Storage(StorageInterface):
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure: bool = False,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                self.client.set_bucket_policy(
                    self.bucket_name,
                    self._get_public_read_policy(),
                )

        except S3Error as e:
            raise Exception(f"Failed to ensure bucket exists: {e}")

    def _get_public_read_policy(self) -> str:
        public_read_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"],
                }
            ],
        }

        return json.dumps(public_read_policy)

    async def save_file(self, file: UploadFile, filename: str) -> str:
        try:
            content = await file.read()

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                data=BytesIO(content),
                length=len(content),
                content_type=file.content_type or "application/octet-stream",
            )

            return filename

        finally:
            await file.close()

    async def delete_file(self, filename: str) -> bool:
        try:
            self.client.remove_object(self.bucket_name, filename)
            return True

        except S3Error:
            return False

        except Exception:
            return False
