# Test: Nginx + PHP-FPM, Terraform, Ansible

This repository is a **template** for completing the test assignment. Full description is in [INSTRUCTIONS.md](./INSTRUCTIONS.md).

## What's already included
- Directory structure for Terraform/Ansible.
- Basic GitHub Actions workflows: `terraform.yml`, `ansible.yml`.
- Template files for `web` role (Ansible) and minimal Terraform configs.

## What the candidate needs to implement (briefly)
1. **Terraform**: describe `nginx` and `php-fpm` containers (docker provider), network and volume, variables and outputs.
2. **Ansible**: `web` role should deploy Nginx config, index.php, enable `nginx` and `php-fpm`, add logrotate.
3. Clean up and complete workflows (fmt/validate/plan + ansible-lint), optionally add Molecule tests for the role.
4. **README**: complete the steps below for running and testing (see "Local Run" section).

---

## Local Run (to be filled after completion)
```bash
# example
cd terraform
terraform init
terraform apply -auto-approve

cd ../ansible
ansible-playbook -i inventory/containers.ini playbooks/site.yml
```

### Testing
```bash
curl http://localhost:8080/healthz
# expected JSON:
# {"status":"ok","service":"nginx","env":"dev"}
```

## CI/CD
- **Actions** tab should be green: Terraform (fmt/validate/plan) and ansible-lint pass.
- Attach screenshots or links to successful runs.

## Useful Links
- Full task description: [INSTRUCTIONS.md](./INSTRUCTIONS.md)
- Solution rationale: `Decisions.md`
