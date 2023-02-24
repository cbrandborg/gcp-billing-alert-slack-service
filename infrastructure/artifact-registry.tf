resource "google_artifact_registry_repository" "registry-client-billing" {
  location      = var.location
  project       = var.project_id
  repository_id = var.artifact_registry
  description   = "Repository for billing projects related to clients"
  format        = "DOCKER"

  depends_on = [
    google_project_service.api_enable-2
  ]
}