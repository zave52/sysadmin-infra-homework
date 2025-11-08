output "nginx_container_name" {
  description = "Name of the nginx container"
  value       = docker_container.nginx.name
}

output "php_fpm_container_name" {
  description = "Name of the PHP-FPM container"
  value       = docker_container.php_fpm.name
}

output "healthz_url" {
  description = "Health check endpoint URL"
  value       = "http://localhost:${var.host_port}/healthz"
}

output "network_name" {
  description = "Docker network name"
  value       = docker_network.app_network.name
}
