resource "google_project_service" "api_enable-1" {
  project = var.project_id

  for_each = toset([
    "cloudapis.googleapis.com",
    "cloudbilling.googleapis.com",
    "iam.googleapis.com",
    "billingbudgets.googleapis.com",

  ])
  service = each.key

  timeouts {
    create = "30m"
    update = "40m"
  }
}

resource "google_project_service" "api_enable-2" {
  project = var.project_id

  for_each = toset([
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",

  ])
  service = each.key

  disable_dependent_services = true

  timeouts {
    create = "30m"
    update = "40m"
  }

  depends_on = [
    google_project_service.api_enable-1
  ]
}

resource "google_service_account" "cloud_run_sa" {
  account_id   = var.cloud_run_sa
  display_name = "Billing Cloud Run Service Account"

  depends_on = [
    google_project_service.api_enable-2
  ]
}


resource "google_cloud_run_service_iam_member" "invoker_cloud_run_sa_member" {
  location = google_cloud_run_service.cloud_run_notification_service.location
  project  = google_cloud_run_service.cloud_run_notification_service.project
  service  = google_cloud_run_service.cloud_run_notification_service.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.cloud_run_sa.email}"

  depends_on = [
    google_service_account.cloud_run_sa,
    google_cloud_run_service.cloud_run_notification_service
  ]
}

resource "google_project_service_identity" "pubsub_service_agent" {
  provider = google-beta
  project  = var.project_id
  service  = "pubsub.googleapis.com"

  depends_on = [
    google_project_service.api_enable-2
  ]
}

resource "google_project_iam_binding" "token_creator_service_agent_member" {
  project = var.project_id
  role    = "roles/iam.serviceAccountTokenCreator"
  members = ["serviceAccount:${google_project_service_identity.pubsub_service_agent.email}"]

  depends_on = [
    google_project_service_identity.pubsub_service_agent
  ]
}