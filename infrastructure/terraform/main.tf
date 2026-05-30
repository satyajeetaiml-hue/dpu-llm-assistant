# Terraform equivalent of the core Azure infrastructure.
# Usage:
#   terraform init
#   terraform apply -var="prefix=uniai" -var="location=eastus"

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "prefix" {
  type    = string
  default = "uniai"
}

variable "location" {
  type    = string
  default = "eastus"
}

resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-rg"
  location = var.location
}

resource "azurerm_storage_account" "main" {
  name                     = "${var.prefix}stor${substr(md5(azurerm_resource_group.main.id), 0, 8)}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
}

resource "azurerm_storage_container" "documents" {
  name                  = "documents"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_search_service" "main" {
  name                = "${var.prefix}-search"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "basic"
}

resource "azurerm_cognitive_account" "openai" {
  name                = "${var.prefix}-openai"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  kind                = "OpenAI"
  sku_name            = "S0"
  custom_subdomain_name = "${var.prefix}-openai"
}

output "openai_endpoint" {
  value = azurerm_cognitive_account.openai.endpoint
}

output "search_service_name" {
  value = azurerm_search_service.main.name
}
