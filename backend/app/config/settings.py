
import os
REDIS_URL = os.getenv("SF_REDIS_URL", "redis://localhost:6379/0")
REGION_ID = os.getenv("SF_REGION_ID", "region-a")
