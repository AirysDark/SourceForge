
import boto3
from botocore.client import Config
from .interface import ObjectStorageBackend
from app.config.settings import S3_BUCKET, S3_REGION, S3_ENDPOINT

class S3Storage(ObjectStorageBackend):
    def __init__(self):
        self.client = boto3.client(
            "s3",
            region_name=S3_REGION,
            endpoint_url=S3_ENDPOINT,
            config=Config(signature_version="s3v4")
        )

    def write(self, key: str, data: bytes):
        self.client.put_object(Bucket=S3_BUCKET, Key=key, Body=data)

    def read(self, key: str):
        try:
            obj = self.client.get_object(Bucket=S3_BUCKET, Key=key)
            return obj["Body"].read()
        except:
            return None

    def delete(self, key: str):
        self.client.delete_object(Bucket=S3_BUCKET, Key=key)

    def list(self):
        resp = self.client.list_objects_v2(Bucket=S3_BUCKET)
        if "Contents" not in resp:
            return []
        return [item["Key"] for item in resp["Contents"]]
