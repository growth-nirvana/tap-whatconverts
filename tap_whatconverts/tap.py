"""WhatConverts tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_whatconverts import streams


class TapWhatConverts(Tap):
    """WhatConverts tap class."""

    name = "tap-whatconverts"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,
            title="API Key",
            description="The api key to authenticate against the API service",
        ),
        th.Property(
            "secret_key",
            th.StringType,
            required=True,
            secret=True,
            title="Secret Key",
            description="The secret key to authenticate against the API service",
        ),
        th.Property(
            "profile_id",
            th.IntegerType,
            required=True,
            title="Profile ID",
            description="The profile id to authenticate against the API service",
        ),
        th.Property(
            "account_id",
            th.IntegerType,
            required=True,
            title="Account ID",
            description="The account id to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.WhatConvertsStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.LeadsStream(self),
            # streams.PhoneTrackingStream(self),
            # streams.WebFormTrackingStream(self),
        ]


if __name__ == "__main__":
    TapWhatConverts.cli()
