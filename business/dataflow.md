# Dataflow Architecture
## Overview
The dataflow architecture for rust-shield is designed to provide a secure and efficient way to build web applications. The following sections outline the different tiers of the architecture.

## External Data Sources
* GitHub API (for repository data)
* Rust crate registry (for dependency data)
* User input (for configuration and code)

## Ingestion Layer
```markdown
+---------------+
|  GitHub API  |
|  Rust Registry|
|  User Input  |
+---------------+
       |
       |
       v
+---------------+
|  API Gateway  |
|  (NGINX/Lua)  |
+---------------+
       |
       |
       v
```
* API Gateway (NGINX/Lua)
* Data Ingestion Service (Rust-based)

## Processing/Transform Layer
```markdown
+---------------+
| Data Ingestion|
|  Service      |
+---------------+
       |
       |
       v
+---------------+
|  Data Processor|
|  (Rust-based)  |
+---------------+
       |
       |
       v
```
* Data Processor (Rust-based)
* Dependency Resolver (Rust-based)
* Code Analyzer (Rust-based)

## Storage Tier
```markdown
+---------------+
|  Data Processor|
|  (Rust-based)  |
+---------------+
       |
       |
       v
+---------------+
|  Database     |
|  (PostgreSQL)  |
+---------------+
       |
       |
       v
```
* Database (PostgreSQL)
* File Storage (S3-compatible)

## Query/Serving Layer
```markdown
+---------------+
|  Database     |
|  (PostgreSQL)  |
+---------------+
       |
       |
       v
+---------------+
|  Query Service |
|  (Rust-based)  |
+---------------+
       |
       |
       v
```
* Query Service (Rust-based)
* API Gateway (NGINX/Lua)

## Egress to User
```markdown
+---------------+
|  Query Service |
|  (Rust-based)  |
+---------------+
       |
       |
       v
+---------------+
|  Web Interface |
|  (React-based) |
+---------------+
       |
       |
       v
```
* Web Interface (React-based)
* CLI Tool (Rust-based)

## Auth Boundaries
* API Gateway (NGINX/Lua) handles authentication and authorization for incoming requests
* Query Service (Rust-based) handles authentication and authorization for database queries
* Web Interface (React-based) handles authentication and authorization for user interactions

## Components per Tier
* External Data Sources:
	+ GitHub API
	+ Rust crate registry
	+ User input
* Ingestion Layer:
	+ API Gateway (NGINX/Lua)
	+ Data Ingestion Service (Rust-based)
* Processing/Transform Layer:
	+ Data Processor (Rust-based)
	+ Dependency Resolver (Rust-based)
	+ Code Analyzer (Rust-based)
* Storage Tier:
	+ Database (PostgreSQL)
	+ File Storage (S3-compatible)
* Query/Serving Layer:
	+ Query Service (Rust-based)
	+ API Gateway (NGINX/Lua)
* Egress to User:
	+ Web Interface (React-based)
	+ CLI Tool (Rust-based)