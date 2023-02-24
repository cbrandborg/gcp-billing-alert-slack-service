
data "google_billing_account" "account" {
    billing_account = var.billing_account

    depends_on = [
        google_project_service.api_enable-2
    ]
}

resource "google_billing_budget" "budget" {
    billing_account = data.google_billing_account.account.id
    display_name = "Main Billing Budget"

    amount {
    last_period_amount = true
    }

    threshold_rules {
        threshold_percent =  1.3
        spend_basis       = "CURRENT_SPEND"
    }

    threshold_rules {
        threshold_percent =  1.5
        spend_basis       = "CURRENT_SPEND"
    }

    threshold_rules {
        threshold_percent =  2.0
        spend_basis       = "FORECASTED_SPEND"
    }

    all_updates_rule {

        pubsub_topic = module.pubsub.id
        disable_default_iam_recipients = false
        
    }

    depends_on = [
        data.google_billing_account.account
    ]
}