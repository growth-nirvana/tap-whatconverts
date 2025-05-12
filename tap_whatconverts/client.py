"""REST client handling, including WhatConvertsStream base class."""

from __future__ import annotations

import decimal
import typing as t
from importlib import resources

from requests.auth import HTTPBasicAuth
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context


class WhatConvertsStream(RESTStream):
    """WhatConverts stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://app.whatconverts.com/api/v1"

    @property
    def authenticator(self) -> HTTPBasicAuth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """

        api_key = self.config["api_key"]
        secret_key = self.config["secret_key"]

        return HTTPBasicAuth(
            username=api_key,
            password=secret_key,
        )

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
        account_id = self.config["account_id"]
        profile_id = self.config["profile_id"]
        start_date = self.config["start_date"]

        params = {
            "leads_per_page": 250,
            "account_id": account_id,
            "profile_id": profile_id,
        }

        if(self.name == "whatconverts_leads"):
            params["start_date"] = start_date

        if next_page_token:
            params["page"] = next_page_token

        return params

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        profile_id = self.config["profile_id"]

        yield from (
            {
                **record,
                "profile_id": profile_id,
            }
            for record in extract_jsonpath(self.records_jsonpath, input=response.json())
        )
