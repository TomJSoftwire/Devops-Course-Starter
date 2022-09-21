terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "Softwire21_ThomasJohnston_ProjectExercise"
    storage_account_name = "tfstate10453"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
provider "azurerm" {
  features {}
}
variable "oauth_app_id" {
  type      = string
  sensitive = true
}
variable "oauth_app_secret" {
  type      = string
  sensitive = true
}
variable "secret_key" {
  type      = string
  sensitive = true
}
variable "prefix" {
  type    = string
  default = "prod"
}
variable "env" {
  type    = string
  default = "production"
}
data "azurerm_resource_group" "main" {
  name = "Softwire21_ThomasJohnston_ProjectExercise"
}
resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}
resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-terraform-todo-app-thojoh"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id
  site_config {
    application_stack {
      docker_image     = "thomasjohnstonsoftwire/todo-app"
      docker_image_tag = "latest"
    }
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGO_CONNECTION_STRING"    = azurerm_cosmosdb_account.main.connection_strings[0]
    "MONGO_DB_NAME"              = "todo-app-storage"
    "FLASK_APP"                  = "todo_app/app"
    "FLASK_ENV"                  = var.env
    "PORT"                       = 80
    "OAUTH_APP_ID"               = var.oauth_app_id
    "OAUTH_APP_SECRET"           = var.oauth_app_secret
    "SECRET_KEY"                 = var.secret_key
  }
}
resource "azurerm_cosmosdb_account" "main" {
  name                 = "${var.prefix}-terraform-cosmos-account"
  kind                 = "MongoDB"
  location             = data.azurerm_resource_group.main.location
  resource_group_name  = data.azurerm_resource_group.main.name
  offer_type           = "Standard"
  mongo_server_version = "4.2"

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

    lifecycle {
      prevent_destroy = true
    }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }
}
resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-terraform-cosmos-mongo-db"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}
output "webapp_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}
output "deployment_trigger" {
  value = "https://${azurerm_linux_web_app.main.site_credential[0].name}:${azurerm_linux_web_app.main.site_credential[0].password}@${azurerm_linux_web_app.main.name}.scm.azurewebsites.net/docker/hook"
}
