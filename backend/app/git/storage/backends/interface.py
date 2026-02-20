
class ObjectStorageBackend:
    def write(self, key: str, data: bytes):
        raise NotImplementedError

    def read(self, key: str):
        raise NotImplementedError

    def delete(self, key: str):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError
