import time
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Tuple, Dict
from collections import defaultdict
from wsgiref.util import setup_testing_defaults

@dataclass
class SecurityConfig:
    """Security configuration for the middleware."""
    csp_policy: str = "default-src 'self';"
    headers: Dict[str, str] = field(default_factory=dict)
    rate_limit: int = 5
    rate_window: int = 60

class SecurityMiddleware:
    """WSGI middleware that provides security defaults."""
    def __init__(self, app: Callable, config: SecurityConfig):
        self.app = app
        self.config = config
        self.request_counts = defaultdict(int)
        self.last_request_times = {}

    def __call__(self, environ, start_response):
        """WSGI application entry point."""
        ip_address = environ.get("REMOTE_ADDR", "unknown")
        current_time = time.time()

        # Rate limiting
        if ip_address in self.request_counts:
            time_diff = current_time - self.last_request_times[ip_address]
            if time_diff < self.config.rate_window:
                self.request_counts[ip_address] += 1
                if self.request_counts[ip_address] > self.config.rate_limit:
                    status = "429 Too Many Requests"
                    headers = [("Content-Type", "text/plain")]
                    start_response(status, headers)
                    return [b"Too Many Requests"]
            else:
                self.request_counts[ip_address] = 1
        else:
            self.request_counts[ip_address] = 1

        self.last_request_times[ip_address] = current_time

        # Add security headers
        def start_response_wrapper(status, headers, exc_info=None):
            headers.append(("Content-Security-Policy", self.config.csp_policy))
            for key, value in self.config.headers.items():
                headers.append((key, value))
            return start_response(status, headers, exc_info)

        return self.app(environ, start_response_wrapper)
