variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "nginx-php-app"
}

variable "host_port" {
  description = "Host port to expose nginx container"
  type        = number
  default     = 8080
}

variable "app_env" {
  description = "Application environment"
  type        = string
  default     = "dev"
}
