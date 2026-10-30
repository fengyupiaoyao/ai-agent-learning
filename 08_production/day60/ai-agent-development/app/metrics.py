from prometheus_client import Counter, Histogram, make_asgi_app

REQUEST_TOTAL = Counter(
    "agent_http_requests",
    "Total HTTP requests",
    ["method", "route", "status"],
)

REQUEST_DURATION = Histogram(
    "agent_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "route"],
)

metrics_app = make_asgi_app()
