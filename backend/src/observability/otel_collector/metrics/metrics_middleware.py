import time
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry.metrics import get_meter


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to collect HTTP request metrics for FastAPI using OpenTelemetry.
    - Exports a counter: http_server_requests_total
    - Exports a histogram: http_request_duration_seconds
    Labels: method, path, status_code
    """
    def __init__(self, app, meter):
        super().__init__(app)
        self.meter = meter
        self._create_metric_instruments()

    def _create_metric_instruments(self):
        """
        Create and initialize metric instruments for HTTP request counting and duration.
        This method sets up:
        - Counter: http_server_requests_total
        - Histogram: http_request_duration_seconds
        """
        # Counter for total HTTP requests
        self.request_counter = self.meter.create_counter(
            name="http_server_requests_total",
            description="Total HTTP requests",
            unit="1"
        )
        
        # Histogram for request duration in seconds
        self.duration_histogram = self.meter.create_histogram(
            name="http_request_duration_seconds",
            description="HTTP request duration in seconds",
            unit="s"
        )

    async def dispatch(self, request, call_next):
        """
        Intercepts each HTTP request to:
        - Record the start time before processing.
        - Call the next handler in the middleware chain (the actual endpoint).
        - Measure the duration of the request.
        - Prepare metric labels (method, path, status_code).
        - Increment the request counter and record the duration histogram.
        - Return the response to the client.

        Example:
            # When a GET request is made to /health and returns 200:
            # - Increments http_server_requests_total with labels:
            #   method="GET", path="/health", status_code="200"
            # - Records the time taken in http_request_duration_seconds with same labels.

        Returns:
            response: The HTTP response from the endpoint.
        """
        # Record the start time
        start_time = time.time()

        # Process the request and get the response
        response = await call_next(request)

        # Calculate request duration
        duration = time.time() - start_time

        # Prepare labels for metrics
        labels = {
            "method": request.method,           # HTTP method (GET, POST, etc.)
            "path": request.url.path,           # Request path
            "status_code": str(response.status_code)  # Response status code
        }

        # Increment the request counter
        self.request_counter.add(1, labels)

        # Record the request duration
        self.duration_histogram.record(duration, labels)
        
        return response

