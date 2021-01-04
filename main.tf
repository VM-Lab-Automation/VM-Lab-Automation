terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.26"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "registry_password" {
  type = string
}

resource "azurerm_resource_group" "rg" {
  name     = "VM_automation"
  location = "westeurope"
}

resource "azurerm_container_registry" "acr" {
  name                     = "vmautomation"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  sku                      = "Basic"
  admin_enabled            = true
}

resource "azurerm_app_service_plan" "plan" {
  name                = "vmlabautomation-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind = "Linux"
  reserved = true

  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "service" {
  name                = "vmlabautomation"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.plan.id

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = false

    DOCKER_REGISTRY_SERVER_URL      = "https://vmautomation.azurecr.io"
    DOCKER_REGISTRY_SERVER_USERNAME = "vmautomation"
    DOCKER_REGISTRY_SERVER_PASSWORD = var.registry_password
  }

  site_config {
    linux_fx_version = "COMPOSE|${filebase64("docker-compose.azure.yml")}" 
  }

}