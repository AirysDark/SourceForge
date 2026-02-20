
from app.config.settings import STORAGE_BACKEND
from .backends.local import LocalStorage
from .backends.s3 import S3Storage

def get_storage():
    if STORAGE_BACKEND == "s3":
        return S3Storage()
    return LocalStorage()
