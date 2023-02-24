variable "organization_id" {
    description = "Project ID for PubSub Topic and Cloud Functions"
}

variable "project_id" {
    description = "Project ID for PubSub Topic and Cloud Functions"
}

variable "billing_account" {
    description = "Main billing account"
}

variable "cloud_run_sa" {
    description = "Service Account name for Cloud Run"
}

variable "location" {
    description = "Location of deployed cloud services"
}

variable tf_state_bucket_name {
    description = "Name of bucket containing terraform statefiles"
}

variable "terraform_sa" {
    description = "General service account for deploying terraform"
}

variable "artifact_registry" {
    description = "Repository for pushing docker images"
}

variable "tf_organization" {
    description = "Storage Bucket for storing Terraform state file"
}

variable "tf_workspace" {
    description = "Prefix path in Storage bucket"
}