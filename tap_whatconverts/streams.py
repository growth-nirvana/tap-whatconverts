"""Stream type classes for tap-whatconverts."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_whatconverts.client import WhatConvertsStream


class AccountsStream(WhatConvertsStream):
    """Define accounts stream."""

    name = "whatconverts_accounts"
    path = "/accounts"
    primary_keys = ["account_id"]
    replication_key = None
    records_jsonpath = "$.accounts[*]"
    schema = th.PropertiesList(
        th.Property("account_id", th.IntegerType),
        th.Property("account_name", th.StringType),
        th.Property("account_status", th.StringType),
        th.Property("account_type", th.StringType),
        th.Property("account_created", th.DateTimeType),
        th.Property("account_updated", th.DateTimeType),
        th.Property("date_created", th.DateTimeType),
    ).to_dict()


class ProfilesStream(WhatConvertsStream):
    """Define profiles stream."""

    name = "whatconverts_profiles"
    path = "/accounts/{account_id}/profiles"
    primary_keys = ["profile_id"]
    replication_key = None
    records_jsonpath = "$.profiles[*]"
    schema = th.PropertiesList(
        th.Property("profile_id", th.IntegerType),
        th.Property("account_id", th.IntegerType),
        th.Property("profile_name", th.StringType),
        th.Property("profile_status", th.StringType),
        th.Property("profile_created", th.DateTimeType),
        th.Property("profile_updated", th.DateTimeType),
        th.Property("date_created", th.DateTimeType),
    ).to_dict()

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = {}
        if next_page_token:
            params["page"] = next_page_token
        return params

    def get_records(self, context: Context | None) -> t.Iterable[dict[str, t.Any]]:
        """Get records from the stream.

        Args:
            context: Stream partition or context dictionary.

        Yields:
            One item per (possibly processed) record in the API.
        """
        # First get all accounts
        accounts_stream = AccountsStream(self._tap)
        for account in accounts_stream.get_records(context):
            account_id = account["account_id"]
            
            # Update the path with the current account_id
            self.path = f"/accounts/{account_id}/profiles"
            
            # Get profiles for this account
            for profile in super().get_records(context):
                yield {
                    **profile,
                    "account_id": account_id,
                }


class LeadsStream(WhatConvertsStream):
    """Define custom stream."""

    name = "whatconverts_leads"
    path = "/leads"
    primary_keys = ["lead_id"]
    replication_key = None
    records_jsonpath = "$.leads[*]"
    schema = th.PropertiesList(
        th.Property("account_id", th.IntegerType),
        th.Property("profile_id", th.IntegerType),
        th.Property("profile", th.StringType),
        th.Property("lead_id", th.IntegerType),
        th.Property("user_id", th.StringType),
        th.Property("lead_type", th.StringType),
        th.Property("lead_status", th.StringType),
        th.Property("date_created", th.DateTimeType),
        th.Property("quotable", th.StringType),
        th.Property("quote_value", th.IntegerType),
        th.Property("sales_value", th.IntegerType),
        th.Property("spotted_keywords", th.StringType),
        th.Property("lead_score", th.IntegerType),
        th.Property("lead_state", th.StringType),
        th.Property("lead_source", th.StringType),
        th.Property("lead_medium", th.StringType),
        th.Property("lead_campaign", th.StringType),
        th.Property("lead_content", th.StringType),
        th.Property("lead_keyword", th.StringType),
        th.Property("lead_url", th.StringType),
        th.Property("landing_url", th.StringType),
        th.Property("operating_system", th.StringType),
        th.Property("browser", th.StringType),
        th.Property("device_type", th.StringType),
        th.Property("device_make", th.StringType),
        th.Property("spam", th.BooleanType),
        th.Property("duplicate", th.BooleanType),
        th.Property("tracking_number", th.StringType),
        th.Property("destination_number", th.StringType),
        th.Property("caller_country", th.StringType),
        th.Property("caller_state", th.StringType),
        th.Property("caller_zip", th.StringType),
        th.Property("caller_name", th.StringType),
        th.Property("call_duration", th.StringType),
        th.Property("call_duration_seconds", th.IntegerType),
        th.Property("caller_city", th.StringType),
        th.Property("answer_status", th.StringType),
        th.Property("call_status", th.StringType),
        th.Property("line_type", th.StringType),
        th.Property("caller_number", th.StringType),
        th.Property("phone_name", th.StringType),
        th.Property("message", th.StringType),
        th.Property("ip_address", th.StringType),
        th.Property("notes", th.StringType),
        th.Property("contact_name", th.StringType),
        th.Property("contact_company_name", th.StringType),
        th.Property("contact_email_address", th.StringType),
        th.Property("contact_phone_number", th.StringType),
        th.Property("email_address", th.StringType),
        th.Property("phone_number", th.StringType),
        th.Property("gclid", th.StringType),
        th.Property("msclkid", th.StringType),
        th.Property("unbounce_page_id", th.StringType),
        th.Property("unbounce_variant_id", th.StringType),
        th.Property("unbounce_visitor_id", th.StringType),
        th.Property("salesforce_user_id", th.IntegerType),
        th.Property("roistat_visit_id", th.StringType),
        th.Property("hubspot_visitor_id", th.StringType),
        th.Property("facebook_browser_id", th.StringType),
        th.Property("facebook_click_id", th.StringType),
        th.Property("vwo_account_id", th.StringType),
        th.Property("vwo_experiment_id", th.StringType),
        th.Property("vwo_variant_id", th.StringType),
        th.Property("vwo_user_id", th.StringType),
        th.Property("google_analytics_client_id", th.StringType),
        th.Property("recording", th.StringType),
        th.Property("play_recording", th.StringType),
        th.Property("voicemail", th.StringType),
        th.Property("play_voicemail", th.StringType),
        th.Property("call_transcription", th.StringType),
        th.Property("voicemail_transcription", th.StringType),
        th.Property("account", th.StringType),
        th.Property("lead_analysis", th.StringType),
        th.Property("last_updated", th.DateTimeType),
        th.Property("additional_fields", th.StringType),
        th.Property("city", th.StringType),
        th.Property("country", th.StringType),
        th.Property("state", th.StringType),
        th.Property("zip", th.StringType),
        th.Property("form_name", th.StringType),
        th.Property("google_analytics_session_id", th.StringType),
    ).to_dict()


class PhoneTrackingStream(WhatConvertsStream):
    """Define custom stream."""

    name = "whatconverts_tracking_phone_numbers"
    path = "/tracking/numbers"
    primary_keys = ["phone_number_id"]
    replication_key = None
    records_jsonpath = "$.numbers[*]"
    schema = th.PropertiesList(
        th.Property("phone_number_id", th.IntegerType),
        th.Property("phone_name", th.StringType),
        th.Property("tracking_number", th.StringType),
        th.Property("tracking_number_iso_country", th.StringType),
        th.Property("destination_number", th.StringType),
        th.Property("destination_number_iso_country", th.StringType),
        th.Property("swap_number", th.StringType),
        th.Property("call_flow", th.StringType),
        th.Property("trigger", th.StringType),
        th.Property("source", th.StringType),
        th.Property("medium", th.StringType),
        th.Property("last_used", th.DateTimeType),
        th.Property("call_recording", th.BooleanType),
        th.Property("voice", th.BooleanType),
        th.Property("messaging", th.BooleanType),
        th.Property("pending_activation", th.BooleanType),
        th.Property("account_id", th.IntegerType),
        th.Property("profile_id", th.IntegerType),
        th.Property("profile", th.StringType),
        th.Property("campaign", th.StringType),
        th.Property("content", th.StringType),
        th.Property("keyword", th.StringType),
    ).to_dict()


class WebFormTrackingStream(WhatConvertsStream):
    """Define custom stream."""

    name = "whatconverts_tracking_web_forms"
    path = "/tracking/forms"
    primary_keys = ["form_id"]
    replication_key = None
    records_jsonpath = "$.forms[*]"
    schema = th.PropertiesList(
        th.Property("form_id", th.IntegerType),
        th.Property("form_name", th.StringType),
        th.Property("attribute_type", th.StringType),
        th.Property("attribute_type_value", th.StringType),
        th.Property("submit_attribute_type", th.StringType),
        th.Property("submit_attribute_type_value", th.StringType),
        th.Property("profile", th.StringType),
        th.Property("profile_id", th.IntegerType),
        th.Property("account_id", th.IntegerType),
    ).to_dict()
