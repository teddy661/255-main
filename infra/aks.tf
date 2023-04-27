
resource "azurerm_kubernetes_cluster" "k8s" {
  name                = "w255-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "w255"

  kubernetes_version = "1.25.4"

  default_node_pool {
    name                = "default"
    min_count           = 1  // 4 CPU, 16 GB memory
    max_count           = 12 // 40 CPU, 160 GB memory
    vm_size             = "standard_d16ls_v5"
    enable_auto_scaling = true
    # os_disk_type        = "Ephemeral"
  }

  auto_scaler_profile {}

  azure_active_directory_role_based_access_control {
    managed            = true
    azure_rbac_enabled = true
  }

  network_profile {
    load_balancer_sku = "standard"
    network_plugin    = "kubenet"
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.test.id
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "acr_access" {
  principal_id                     = azurerm_kubernetes_cluster.k8s.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}
