"""Stream type classes for tap-whatconverts."""

from __future__ import annotations

import typing as t
from importlib import resources
from singer_sdk import typing as th
from tap_whatconverts.client import WhatConvertsStream


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
