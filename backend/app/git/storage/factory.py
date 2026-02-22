# backend/app/git/storage/factory.py

from app.config.settings import STORAGE_BACKEND
from .backends.local import LocalStorage


def get_storage():
    """
    Storage backend factory.
    Supported backends:
      - local
      - s3
    """

    backend = STORAGE_BACKEND.lower()

    if backend == "local":
        return LocalStorage()

    if backend == "s3":
        try:
            from .backends.s3 import S3Storage
        except ImportError:
            raise RuntimeError(
                "S3 backend selected but dependencies not installed."
            )
        return S3Storage()

    raise ValueError(f"Invalid STORAGE_BACKEND: {STORAGE_BACKEND}")