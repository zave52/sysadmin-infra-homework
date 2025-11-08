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
