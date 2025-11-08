# Design Decisions

## 1. Variables and Default Values

Variables chosen:

- `project_name` (default: "nginx-php-app") - allows multiple deployments without conflicts
- `host_port` (default: 8080) - non-privileged port, no sudo required
- `app_env` (default: "dev") - safe default for local development

## 2. Nginx and PHP-FPM Connection

Choice: TCP connection via Docker network (`php-fpm:9000`)

Why:

- Simpler than Unix socket in containerized environment
- No shared volume needed for socket file
- Docker network provides automatic DNS resolution
- Standard PHP-FPM port (9000)

Alternative considered: Unix socket would require additional volume sharing between containers, adding complexity.

## 3. Ansible Idempotency

Implementation:

- Conditional installation: `when: logrotate_check.rc != 0`
- Changed flags: `changed_when: false` for validation tasks
- Content-based deployments: only trigger handlers when files actually change
- Handler design: nginx reload only fires when configuration changes

## 4. Health Check Endpoint

What `/healthz` checks:

- PHP-FPM is running (502/504 if down)
- Network connectivity between nginx and php-fpm
- Environment variable propagation (`APP_ENV`)
- File system access (PHP file must be readable)

## 5. Logrotate Implementation

Choice: Install logrotate inside nginx container via Ansible

Why:

- Uses official Docker images
- Configuration managed as code (Ansible)
- Self-contained (no host dependencies)

## 6. Local CI Testing with Act

Choice: Document Act usage for local GitHub Actions testing

Why:

- Faster feedback loop (no push required)
- Consistent behavior between local and CI environments
- Debug complex workflows locally before pushing
- Uses same container-based approach as GitHub runners

Trade-off: Requires Docker and may have minor differences from GitHub's actual runner environment

## Future Improvements

- Multi-environment configuration
- Security hardening (non-root users, read-only filesystem)
- Monitoring and metrics
- Backup for volumes and configuration
- Performance tuning (PHP-FPM pools, Nginx caching, connection limits)