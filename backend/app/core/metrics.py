
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

REQUEST_COUNT = Counter(
    "sf_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "sf_http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"]
)

ACTIVE_REFS = Gauge(
    "sf_active_refs_total",
    "Total active refs in system"
)

def track_request(method, endpoint):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

def track_latency(endpoint, duration):
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)

def set_active_refs(count):
    ACTIVE_REFS.set(count)

def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
