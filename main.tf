terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
}
provider "azurerm" {
  features {}
}
variable "oauth_app_id" {
  type = string
}
variable "oauth_app_secret" {
  type = string
}
data "azurerm_resource_group" "main" {
  name = "Softwire21_ThomasJohnston_ProjectExercise"
}
resource "azurerm_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}
resource "azurerm_linux_web_app" "main" {
  name                = "terraform-todo-app-thojoh"
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
    "OAUTH_APP_ID"               = var.oauth_app_id
    "OAUTH_APP_SECRET"           = var.oauth_app_secret
  }
}
resource "azurerm_cosmosdb_account" "main" {
  name                = "terraform-cosmos-account"
  kind                = "MongoDB"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  mongo_server_version = "3.6"

  capabilities {
    name = "EnableServerless"
  }

  geo_location {
    location          = "northeurope"
    failover_priority = 0
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }
}
resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "terraform-cosmos-mongo-db"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  throughput          = 400
}
