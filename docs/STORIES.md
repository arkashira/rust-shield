# STORIES.md

## Project Overview
**rust‑shield** is a Rust‑based web development platform that delivers secure, high‑performance web applications. The platform bundles a lightweight web framework, a type‑safe routing system, a built‑in authentication layer, and a zero‑config deployment pipeline. The goal of this release is to ship a minimal, production‑ready stack that developers can drop into any Rust project and start building secure web services within minutes.

---

## Epics & Story Backlog

| Epic | Story | Acceptance Criteria |
|------|-------|---------------------|
| **Core Engine** | **E1‑S1** As a developer, I want a lightweight, zero‑config web framework so that I can start building routes without boilerplate. | • `rust-shield` exposes a `ShieldApp::new()` builder.<br>• The app compiles with `cargo build` and runs with `cargo run`.<br>• A default `/health` endpoint returns `200 OK` with JSON `{"status":"ok"}`. |
| | **E1‑S2** As a developer, I want type‑safe routing so that compile‑time errors catch invalid paths. | • Routes are defined via `app.route::<GET, "/users">(|req| ...)`.<br>• Invalid path patterns (e.g., duplicate routes) fail at compile time.<br>• Unit tests cover route resolution for 5 distinct endpoints. |
| | **E1‑S3** As a developer, I want middleware support so that I can inject request/response logic. | • Middleware can be added with `app.middleware(|req, next| ...)`.<br>• Middleware can modify request headers and response status.<br>• A test middleware logs each request to `stdout`. |
| **Security Layer** | **E2‑S1** As a security engineer, I want built‑in CSRF protection so that forms are safe from cross‑site attacks. | • CSRF token is automatically generated per session.<br>• POST requests must include `X-CSRF-Token` header matching the session token.<br>• A failing CSRF check returns `403 Forbidden`. |
| | **E2‑S2** As a security engineer, I want HTTPS enforcement so that all traffic is encrypted. | • The server listens on `https://` by default.<br>• HTTP requests are redirected to HTTPS.<br>• Self‑signed certificates are generated for local dev. |
| | **E2‑S3** As a developer, I want JWT authentication so that I can protect API endpoints. | • `ShieldAuth::jwt(secret)` registers a JWT guard.<br>• Protected routes return `401 Unauthorized` when token is missing or invalid.<br>• A test user can log in and receive a valid JWT. |
| **Deployment Pipeline** | **E3‑S1** As a DevOps engineer, I want a Dockerfile that builds the app in a single layer so that deployments are fast. | • Dockerfile uses `rust:1.75-slim` base.<br>• `cargo build --release` runs in one layer.<br>• The resulting image size is < 200 MB. |
| | **E3‑S2** As a DevOps engineer, I want a CI pipeline that runs tests and lints on every PR. | • GitHub Actions workflow triggers on `push` and `pull_request`.<br>• Workflow runs `cargo test`, `cargo clippy`, and `cargo fmt --check`.<br>• The workflow fails if any step fails. |
| | **E3‑S3** As a DevOps engineer, I want a zero‑config deployment script so that I can deploy to any Kubernetes cluster. | • `deploy.sh` accepts `--namespace` and `--image` flags.<br>• Script generates a Deployment and Service YAML.<br>• `kubectl apply -f` deploys the app without manual edits. |
| **Developer Experience** | **E4‑S1** As a developer, I want auto‑completion for routes in VS Code so that I can write routes faster. | • A `rust-shield` language server provides route suggestions.<br>• Suggestions include HTTP method and path.<br>• VS Code extension is available on the marketplace. |
| | **E4‑S2** As a developer, I want detailed error messages for validation failures so that I can debug quickly. | • Validation errors return JSON with `error` and `details` fields.<br>• Stack traces are suppressed in production builds.<br>• A unit test verifies error format. |
| | **E4‑S3** As a developer, I want a CLI tool to scaffold a new project so that I can bootstrap quickly. | • `cargo install rust-shield-cli` installs the tool.<br>• `rust-shield new myapp` creates a minimal project structure.<br>• Generated project compiles and runs with `cargo run`. |
| **Performance & Monitoring** | **E5‑S1** As a performance engineer, I want built‑in request metrics so that I can monitor latency. | • `/metrics` endpoint returns Prometheus‑compatible metrics.<br>• Metrics include request count, latency histogram, and error rate.<br>• A test verifies metric output contains `http_requests_total`. |
| | **E5‑S2** As a performance engineer, I want async request handling so that the server scales under load. | • All handlers are async functions returning `impl Future`.<br>• The server uses `tokio` runtime with 4 worker threads.<br>• Benchmark shows > 10k RPS on a single core. |
| | **E5‑S3** As a performance engineer, I want graceful shutdown so that in‑flight requests finish before exit. | • SIGINT triggers graceful shutdown.<br>• Server stops accepting new connections after 5 s.<br>• A test simulates shutdown while a request is in flight. |

---

## MVP Release Order

1. **Core Engine** (E1‑S1, S2, S3) – foundational routing and middleware.
2. **Security Layer** (E2‑S1, S2, S3) – CSRF, HTTPS, JWT.
3. **Deployment Pipeline** (E3‑S1, S2, S3) – Docker, CI, Kubernetes deploy script.
4. **Developer Experience** (E4‑S1, S2, S3) – IDE support, error handling, CLI scaffold.
5. **Performance & Monitoring** (E5‑S1, S2, S3) – metrics, async, graceful shutdown.

---

## Acceptance Test Checklist

- All unit tests in `tests/` pass with `cargo test`.
- Lint passes: `cargo clippy --all-targets --all-features -- -D warnings`.
- Formatting passes: `cargo fmt --check`.
- Docker image builds: `docker build -t rust-shield .`.
- CI workflow runs locally with `act`.
- Generated project from CLI compiles and starts a server on `localhost:8080`.

---

## Notes for the Team

- **Documentation**: Update `README.md` with usage examples for each feature.
- **Versioning**: Follow semantic versioning; bump patch for each new feature.
- **Release**: Tag the first stable release as `v0.1.0` and publish to crates.io.
- **Community**: Create a GitHub Discussions board for user questions.

---
