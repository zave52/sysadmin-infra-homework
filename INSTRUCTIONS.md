# Test Assignment: Nginx + PHP-FPM, Terraform, Ansible

**Deadline:** 24 hours (home/offline)  
**Goal:** accuracy, idempotency and basic IaC on Nginx + PHP-FPM stack.  

---

## Task (what needs to be done)

1) **Terraform (docker provider)**
- Describe 2 containers:
  - `nginx` — publishes port **8080** on host.
  - `php-fpm` — processes PHP scripts from shared volume `/var/www/html`.
- Connect containers with shared network (Docker network) and volume.
- Nginx should process PHP via `fastcgi_pass` to `php-fpm` (unix-socket or 127.0.0.1:9000 inside network).
- Serve `index.php` on `/`.
- Return **JSON** on `GET /healthz` like:
  ```json
  {"status":"ok","service":"nginx","env":"<APP_ENV value>"}
  ```
  `APP_ENV` taken from environment variable (default value `dev`).
- **Terraform variables**: `project_name` (string), `host_port` (number, default 8080), `app_env` (string, default `dev`).
- **Outputs**: container names, published port, URL `http://localhost:<port>/healthz`.
- Quality requirements: `terraform fmt`, `terraform validate`, idempotent `apply` (second run without changes).

2) **Ansible**
- Role `roles/web/` that:
  - deploys Nginx config (server on 80, `.php` processing, `location /healthz` returns JSON);
  - deploys `index.php` (mini-script, prints JSON with `APP_ENV`);
  - enables `php-fpm` and `nginx`, configures handlers (restart on changes);
  - configures simple `logrotate` for `/var/log/nginx/*log`.
- Inventory: `ansible/inventory/containers.ini` (allowed `ansible_connection=local` and task execution on localhost if you configure packages on host system; also possible to use `community.docker.docker_container`/`docker exec` for deployment inside container — your choice, main thing is functionality).
- Playbook `ansible/playbooks/site.yml` applies role to target host.
- Idempotency: second playbook run should not make changes.

3) **CI/CD (GitHub Actions)**
- `.github/workflows/terraform.yml`: `terraform fmt -check`, `terraform init`, `terraform validate`, `terraform plan -out=tfplan` (save `tfplan` artifact).
- `.github/workflows/ansible.yml`: `ansible-lint` (mandatory). If you can — add Molecule tests for the role (bonus points).
- In README describe how to test locally and what successful CI runs look like.

---

## What to submit
- Public GitHub repository with this structure (can fork this template).
- Completed `README.md` (see "What candidate should fill" section below).
- Screenshots/links to successful GitHub Actions runs.
- Short `Decisions.md` (3-5 points: key decisions and trade-offs).

Good luck!
