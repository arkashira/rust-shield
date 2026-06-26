# rust-shield
`rust-shield` is a lightweight WSGI middleware that provides security defaults for Python web applications:
* **Content Security Policy (CSP)** – a safe‑by‑default CSP header is added to every response.
* **Rate limiting** – blocks requests that exceed a configurable threshold per IP address.
* **Configurable headers** – add any additional security headers via `SecurityConfig`.
## Installation
No external dependencies are required. Simply copy the `src/` directory into your project.
## Usage
