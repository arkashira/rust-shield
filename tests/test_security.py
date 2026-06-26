import pytest
from wsgiref.util import setup_testing_defaults
from src.security import SecurityMiddleware, SecurityConfig

def simple_app(environ, start_response):
    """A minimal WSGI application that returns 200 OK."""
    status = "200 OK"
    headers = [("Content-Type", "text/plain")]
    start_response(status, headers)
    return [b"Hello World"]

def call_app(app, environ):
    """Helper to call a WSGI app and capture status, headers, and body."""
    captured = {}
    def start_response(status, headers, exc_info=None):
        captured["status"] = status
        captured["headers"] = headers
        return lambda data: None
    result = app(environ, start_response)
    body = b"".join(result)
    return captured["status"], captured["headers"], body

@pytest.fixture
def environ():
    env = {}
    setup_testing_defaults(env)
    env["REMOTE_ADDR"] = "1.2.3.4"
    return env

def test_csp_header_default(environ):
    config = SecurityConfig()
    middleware = SecurityMiddleware(simple_app, config)
    status, headers, body = call_app(middleware, environ)
    assert status == "200 OK"
    header_dict = dict(headers)
    assert "Content-Security-Policy" in header_dict
    assert header_dict["Content-Security-Policy"] == "default-src 'self';"
    assert body == b"Hello World"

def test_rate_limiting(environ):
    config = SecurityConfig(rate_limit=5, rate_window=60)
    middleware = SecurityMiddleware(simple_app, config)
    # Make 5 allowed requests
    for i in range(5):
        status, headers, body = call_app(middleware, environ)
        assert status == "200 OK"
        assert body == b"Hello World"
    # 6th request should be blocked
    status, headers, body = call_app(middleware, environ)
    assert status == "429 Too Many Requests"
    assert body == b"Too Many Requests"
    header_dict = dict(headers)
    assert "Content-Security-Policy" not in header_dict  # 429 response bypasses CSP

def test_custom_config(environ):
    custom_policy = "default-src 'none'; script-src 'self';"
    custom_headers = {"X-Frame-Options": "DENY"}
    config = SecurityConfig(
        csp_policy=custom_policy,
        headers=custom_headers,
        rate_limit=10,
        rate_window=60,
    )
    middleware = SecurityMiddleware(simple_app, config)
    status, headers, body = call_app(middleware, environ)
    assert status == "200 OK"
    header_dict = dict(headers)
    assert header_dict["Content-Security-Policy"] == custom_policy
    assert header_dict["X-Frame-Options"] == "DENY"
    assert body == b"Hello World"

def test_missing_ip(environ):
    # Remove REMOTE_ADDR to test default IP handling
    environ.pop("REMOTE_ADDR", None)
    config = SecurityConfig(rate_limit=1, rate_window=60)
    middleware = SecurityMiddleware(simple_app, config)
    # First request allowed
    status, headers, body = call_app(middleware, environ)
    assert status == "200 OK"
    # Second request should be blocked
    status, headers, body = call_app(middleware, environ)
    assert status == "429 Too Many Requests"
