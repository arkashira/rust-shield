# TECH_SPEC.md

## Rust‑Shield – Technical Specification

**Project**: `rust-shield`  
**Owner**: Axentx Product Team  
**Version**: 0.1.0 (alpha)  
**Last Updated**: 2026‑06‑20  

---

## 1. Overview

Rust‑Shield is a **Rust‑based web development platform** that abstracts common web‑app concerns (routing, state, persistence, authentication, etc.) behind a type‑safe, compile‑time‑checked API. The platform is designed to:

- **Guarantee security** through Rust’s ownership model and built‑in safety guarantees.
- **Enable rapid iteration** with a minimal runtime footprint and zero‑cost abstractions.
- **Scale horizontally** with a stateless request‑handler and pluggable storage back‑ends.

The platform is intended for internal use by Axentx’s autonomous AI‑workforce to prototype and ship web services quickly while ensuring compliance with our security and performance standards.

---

## 2. Architecture

```
┌───────────────────────┐
│  Client (Browser/CLI) │
└─────────────┬─────────┘
              │ HTTP(S)
              ▼
┌───────────────────────┐
│  Rust‑Shield Runtime   │
│  (Actix‑Web + Shield)  │
└───────┬───────┬───────┘
        │       │
        │       └─► 3rd‑party Services
        │
        │
        ▼
┌───────────────────────┐
│  Storage Layer         │
│  (PostgreSQL / Redis)  │
└───────────────────────┘
```

### 2.1 Runtime Layer

| Component | Responsibility | Implementation |
|-----------|----------------|----------------|
| **Actix‑Web** | HTTP server, routing, middleware | `actix-web` 4.x |
| **Shield Core** | Request lifecycle, state management, error handling | Custom crate `shield-core` |
| **Auth Module** | JWT/OIDC, session, RBAC | `jsonwebtoken`, `actix-identity` |
| **Validation** | Request/response schema validation | `serde`, `validator` |
| **Logging** | Structured logging, request tracing | `tracing`, `tracing-actix-web` |
| **Metrics** | Prometheus metrics | `prometheus`, `actix-web-prometheus` |

### 2.2 Storage Layer

| Storage | Use‑case | Driver |
|---------|----------|--------|
| **PostgreSQL** | Relational data, migrations | `sqlx` (async, compile‑time checked) |
| **Redis** | Cache, session store | `deadpool-redis` |
| **File System** | Static assets, uploads | `tokio::fs` |

### 2.3 Deployment Layer

- **Container**: Docker image `rust-shield:latest`
- **Orchestration**: Kubernetes (Helm chart `rust-shield`)
- **CI/CD**: GitHub Actions – lint, test, build, push
- **Observability**: Prometheus, Grafana, Loki

---

## 3. Core Components

| Module | API | Notes |
|--------|-----|-------|
| `shield-core` | `ShieldApp`, `ShieldRoute`, `ShieldError` | Core framework, exposes `ShieldBuilder` |
| `shield-auth` | `AuthMiddleware`, `JwtClaims`, `RoleGuard` | JWT/OIDC integration |
| `shield-db` | `DbPool`, `QueryBuilder`, `Transaction` | SQLx helpers |
| `shield-middleware` | `Cors`, `RateLimiter`, `RequestId` | Custom middleware stack |
| `shield-metrics` | `PrometheusExporter`, `MetricsMiddleware` | Prometheus integration |
| `shield-templates` | `TemplateEngine`, `TemplateContext` | Tera or Askama templates |
| `shield-static` | `StaticFiles`, `AssetCache` | Static file serving |

---

## 4. Data Model

### 4.1 Domain Entities

| Entity | Table | Fields | Constraints |
|--------|-------|--------|-------------|
| `User` | `users` | `id: Uuid`, `email: String`, `password_hash: String`, `role: Role`, `created_at: DateTime<Utc>` | Unique email, password hashed with Argon2 |
| `Session` | `sessions` | `id: Uuid`, `user_id: Uuid`, `expires_at: DateTime<Utc>` | Foreign key to `users` |
| `Post` | `posts` | `id: Uuid`, `author_id: Uuid`, `title: String`, `body: Text`, `published_at: Option<DateTime<Utc>>` | FK to `users` |
| `Comment` | `comments` | `id: Uuid`, `post_id: Uuid`, `author_id: Uuid`, `body: Text`, `created_at: DateTime<Utc>` | FK to `posts`, `users` |

### 4.2 DTOs

- `UserDTO` – public representation of `User` (no password)
- `PostDTO` – includes author info
- `CommentDTO` – includes author info

All DTOs derive `serde::Serialize` / `Deserialize` and `validator::Validate`.

---

## 5. Key APIs / Interfaces

### 5.1 Public API

| Path | Method | Description | Request | Response |
|------|--------|-------------|---------|----------|
| `/api/v1/users` | POST | Register new user | `RegisterUserRequest` | `UserDTO` |
| `/api/v1/auth/login` | POST | Login, returns JWT | `LoginRequest` | `LoginResponse` |
| `/api/v1/posts` | GET | List posts | `QueryParams` | `Vec<PostDTO>` |
| `/api/v1/posts` | POST | Create post | `CreatePostRequest` | `PostDTO` |
| `/api/v1/posts/{id}` | GET | Get post | N/A | `PostDTO` |
| `/api/v1/posts/{id}/comments` | POST | Add comment | `CreateCommentRequest` | `CommentDTO` |

### 5.2 Internal Interfaces

- `DbPool` – async connection pool interface
- `AuthService` – JWT generation & verification
- `RateLimiter` – token bucket per IP
- `Cache` – generic key‑value interface (Redis)

---

## 6. Technology Stack

| Layer | Library | Version | Rationale |
|-------|---------|---------|-----------|
| **Runtime** | `actix-web` | 4.6 | High‑performance async web framework |
| **Database** | `sqlx` | 0.7 | Compile‑time SQL checks, async |
| **Auth** | `jsonwebtoken` | 9.2 | JWT handling |
| **Password** | `argon2` | 0.5 | Secure hashing |
| **Validation** | `validator` | 0.16 | Declarative field validation |
| **Logging** | `tracing` | 0.1 | Structured async logging |
| **Metrics** | `prometheus` | 0.13 | Prometheus exporter |
| **Testing** | `tokio-test`, `mockall` | N/A | Async test utilities |
| **CI** | GitHub Actions | N/A | Build, test, lint |
| **Container** | Docker | N/A | OCI image |
| **Orchestration** | Kubernetes | N/A | Deployment, scaling |

---

## 7. Dependencies

| Crate | Purpose | License |
|-------|---------|---------|
| `actix-web` | HTTP server | MIT |
| `sqlx` | Async SQL | MIT |
| `serde` | Serialization | MIT |
| `serde_json` | JSON handling | MIT |
| `validator` | Input validation | MIT |
| `jsonwebtoken` | JWT | MIT |
| `argon2` | Password hashing | MIT |
| `tracing` | Logging | MIT |
| `prometheus` | Metrics | MIT |
| `deadpool-redis` | Redis pool | MIT |
| `tokio` | Async runtime | MIT |
| `clap` | CLI args | MIT |
| `dotenvy` | Env vars | MIT |

All dependencies are vetted for security and compliance with Axentx’s open‑source policy.

---

## 8. Deployment

### 8.1 Dockerfile

```dockerfile
# Stage 1: Build
FROM rust:1.78-slim-bullseye AS builder
WORKDIR /app
COPY . .
RUN cargo build --release

# Stage 2: Runtime
FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/rust-shield /usr/local/bin/rust-shield
EXPOSE 8080
ENTRYPOINT ["rust-shield"]
```

### 8.2 Helm Chart (`charts/rust-shield/values.yaml`)

```yaml
replicaCount: 3
image:
  repository: ghcr.io/axentx/rust-shield
  tag: latest
service:
  type: ClusterIP
  port: 80
env:
  DATABASE_URL: "postgres://user:pass@db:5432/rustshield"
  REDIS_URL: "redis://redis:6379"
  JWT_SECRET: "REPLACE_ME"
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

### 8.3 CI Pipeline

```yaml
name: Rust Shield CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions-rs/toolchain@v1
        with:
          toolchain: stable
          override: true
      - name: Cache Cargo
        uses: actions/cache@v4
        with:
          path: ~/.cargo/registry
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
      - name: Run tests
        run: cargo test --all
      - name: Build
        run: cargo build --release
      - name: Docker build
        run: docker build -t rust-shield:${{ github.sha }} .
      - name: Push Docker image
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.GHCR_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker tag rust-shield:${{ github.sha }} ghcr.io/axentx/rust-shield:${{ github.sha }}
          docker push ghcr.io/axentx/rust-shield:${{ github.sha }}
```

---

## 9. Security Considerations

- **Input Validation**: All incoming JSON is validated via `validator` before deserialization.
- **Authentication**: JWT signed with HS256; secret stored in Kubernetes secrets.
- **Rate Limiting**: Token bucket per IP, configurable via env.
- **Secrets Management**: Use Vault/K8s secrets; never hard‑code.
- **Audit Logging**: Every request logged with `tracing` and sent to Loki.

---

## 10. Testing Strategy

| Layer | Test Type | Tool | Coverage |
|-------|-----------|------|----------|
| Unit | Logic | `cargo test` | 90% |
| Integration | End‑to‑end | `actix-web::test` | 80% |
| Contract | API | `cargo test` + `serde_json` | 95% |
| Performance | Load | `wrk` + `k6` | 99% |

Automated tests run on every PR; manual exploratory testing is scheduled bi‑weekly.

---

## 11. Roadmap (Next 3 Months)

1. **Feature**: GraphQL API layer (preview) – 1 month
2. **Feature**: WebSocket support for real‑time updates – 1 month
3. **Feature**: CI/CD pipeline for automated Helm chart promotion – 1 month

---

## 12. Appendices

### 12.1 License

MIT – see `LICENSE` file.

### 12.2 Contact

- **Product Lead**: Jane Doe (`jane.doe@axentx.com`)
- **Engineering Lead**: John Smith (`john.smith@axentx.com`)

---
