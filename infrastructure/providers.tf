terraform {

    cloud {
        organization = "cbrandborg"
        
        workspaces {
        name = "billing-slack-notification-service"
        }
    }

    required_providers {
        google = {
        source  = "hashicorp/google"
        version = "4.44.1"
        }
    }
}

provider "google" {

    project = var.project_id
    credentials = file("../prj-dtdk-client-billing-c16970e43cd0.json")
}
