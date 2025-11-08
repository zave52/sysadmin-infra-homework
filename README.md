# Nginx + PHP-FPM, Terraform, Ansible

Test assignment for System Administrator position

## Prerequisites

- Docker
- Terraform (>= 1.6.0)
- Ansible (>= 2.12)
- Python 3.x
- Act (optional, for local CI testing)

## Local Run

### 1. Deploy Infrastructure

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

### 2. Configure with Ansible

```bash
cd ../ansible
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i inventory/containers.ini playbooks/site.yml
```

### 3. Testing

```bash
curl http://localhost:8080/healthz

# Expected response:
# {"status":"ok","service":"nginx","env":"dev"}

curl http://localhost:8080/
```

## Verification

### Containers Running

```bash
docker ps --filter "name=nginx-php-app"
```

### Logrotate Configuration

```bash
# Check logrotate installed
docker exec nginx-php-app-nginx which logrotate

# Check cron running
docker exec nginx-php-app-nginx pgrep cron

# View configuration
docker exec nginx-php-app-nginx cat /etc/logrotate.d/nginx

# Test rotation
docker exec nginx-php-app-nginx logrotate -f /etc/logrotate.conf
docker exec nginx-php-app-nginx ls -la /var/log/nginx/
```

### Idempotency

```bash
cd terraform
terraform apply -auto-approve

# Ansible - second run should show changed=0
cd ../ansible
ansible-playbook -i inventory/containers.ini playbooks/site.yml
```

## CI/CD Testing

### GitHub Actions

Workflows run automatically on push/pull request:

- **terraform.yml**: `fmt -check`, `init`, `validate`, `plan` (uploads tfplan artifact)
- **ansible.yml**: `ansible-lint`, Molecule tests with testinfra verification

[![Terraform](https://github.com/zave52/sysadmin-infra-homework/actions/workflows/terraform.yml/badge.svg)](https://github.com/zave52/sysadmin-infra-homework/actions/workflows/terraform.yml)
[![Ansible](https://github.com/zave/sysadmin-infra-homework/actions/workflows/ansible.yml/badge.svg)](https://github.com/zave52/sysadmin-infra-homework/actions/workflows/ansible.yml)

### Local CI Testing with Act

[Act](https://github.com/nektos/act) allows you to test GitHub Actions workflows locally before pushing to GitHub. It
uses Docker to run the same workflow jobs that would run in GitHub Actions.

Usage:

```bash
# Run all workflows
act

# Run specific workflow
act -W .github/workflows/terraform.yml
act -W .github/workflows/ansible.yml

# Run specific job
act -j lint
act -j terraform
```

## Cleanup

```bash
cd terraform
terraform destroy -auto-approve
```

## Links

- Task description: [INSTRUCTIONS.md](./INSTRUCTIONS.md)
- Design decisions: [Decisions.md](./Decisions.md)

