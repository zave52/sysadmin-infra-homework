terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
  required_version = ">= 1.6.0"
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "app_network" {
  name   = "${var.project_name}-network"
  driver = "bridge"

  labels {
    label = "project"
    value = var.project_name
  }
}

resource "docker_volume" "web_content" {
  name = "${var.project_name}-web-content"

  labels {
    label = "project"
    value = var.project_name
  }
}

resource "docker_volume" "nginx_logs" {
  name = "${var.project_name}-nginx-logs"

  labels {
    label = "project"
    value = var.project_name
  }
}

resource "docker_image" "nginx" {
  name         = "nginx:1.29.3"
  keep_locally = false
}


resource "docker_container" "nginx" {
  name  = "${var.project_name}-nginx"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = var.host_port
  }

  networks_advanced {
    name = docker_network.app_network.name
  }

  volumes {
    volume_name    = docker_volume.web_content.name
    container_path = "/var/www/html"
  }

  volumes {
    host_path      = docker_volume.nginx_logs.name
    container_path = "/var/log/nginx"
  }

  restart = "unless-stopped"

  labels {
    label = "project"
    value = var.project_name
  }

  depends_on = [docker_container.php_fpm]
}

resource "docker_image" "php-fpm" {
  name         = "php:8.4-fpm-alpine"
  keep_locally = false
}


resource "docker_container" "php_fpm" {
  name  = "${var.project_name}-php-fpm"
  image = docker_image.php-fpm.image_id

  networks_advanced {
    name = docker_network.app_network.name
  }

  volumes {
    volume_name    = docker_volume.web_content.name
    container_path = "/var/www/html"
  }

  env = [
    "APP_ENV=${var.app_env}"
  ]

  restart = "unless-stopped"

  labels {
    label = "project"
    value = var.project_name
  }
}
