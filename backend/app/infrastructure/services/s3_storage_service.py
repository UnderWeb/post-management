# backend/app/infrastructure/services/s3_storage_service.py
"""S3-compatible storage service using boto3."""

from __future__ import annotations

from typing import BinaryIO
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError

from app.application.ports.storage_service import StoragePort
from app.core.config.settings import settings


class S3StorageService(StoragePort):
    """
    S3-compatible storage implementation.

    Works with AWS S3 or MinIO for local development.
    """

    def __init__(self) -> None:
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
        )
        self.bucket_name = settings.s3_bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        """Create the S3 bucket if it does not exist."""
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket_name)

    def save_file(self, file_data: BinaryIO, path: str) -> str:
        """Persist a file to S3 and return its object key."""
        extension = path.rsplit(".", 1)[-1] if "." in path else ""
        filename = f"{uuid4()}.{extension}" if extension else str(uuid4())

        self.client.upload_fileobj(file_data, self.bucket_name, filename)

        return filename

    def delete_file(self, path: str) -> bool:
        """Delete a file from S3."""
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=path)
            return True
        except ClientError:
            return False
