from fastapi import APIRouter

router = APIRouter()


@router.get("/fabric/buckets")
def buckets():
    return ["cold-core", "repo-archive"]


@router.get("/fabric/buckets/{bucket}/objects")
def objects(bucket: str):
    return [
        {"name": "repo-001.tar"},
        {"name": "snapshot.img"},
    ]
