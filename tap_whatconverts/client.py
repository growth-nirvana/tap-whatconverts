"""REST client handling, including WhatConvertsStream base class."""

from __future__ import annotations

import decimal
import typing as t
from importlib import resources
import logging
from datetime import datetime

from requests.auth import HTTPBasicAuth
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context

logger = logging.getLogger(__name__)

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

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: t.Any | None,
    ) -> t.Any | None:
        """Return a token for identifying next page or None if no more pages.

        Args:
            response: The HTTP ``requests.Response`` object.
            previous_token: The previous page token value.

        Returns:
            The next pagination token.
        """
        if self.name == "whatconverts_leads":
            # Get total leads count from response
            response_json = response.json()
            total_pages = response_json.get("total_pages", 0)
            current_page = previous_token or 1
            
            # Get the leads from this page
            records = list(extract_jsonpath(self.records_jsonpath, input=response_json))
            if not records:
                return None
                
            # If we have more pages to fetch, return next page number
            if current_page < total_pages:
                return current_page + 1
            return None
        return None

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
        params = {
            "leads_per_page": 250,
            "order": "asc",  # Get oldest leads first
        }

        # Only add account_id and profile_id if they are provided in config
        if "account_id" in self.config:
            params["account_id"] = self.config["account_id"]
        if "profile_id" in self.config:
            params["profile_id"] = self.config["profile_id"]

        if self.name == "whatconverts_leads" and "start_date" in self.config:
            start_date = self.config["start_date"]
            
            # Format the date as YYYY-MM-DD
            if isinstance(start_date, str):
                formatted_date = start_date.split("T")[0]
            else:
                formatted_date = start_date.strftime("%Y-%m-%d")
            
            # Add start_date parameter
            params["start_date"] = formatted_date
            
            # Add end_date as current date to ensure we get all leads up to now
            end_date = datetime.utcnow().strftime("%Y-%m-%d")
            params["end_date"] = end_date

        if next_page_token:
            params["page_number"] = next_page_token

        return params

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # Only add profile_id to records if it's provided in config
        if "profile_id" in self.config:
            yield from (
                {
                    **record,
                    "profile_id": self.config["profile_id"],
                }
                for record in extract_jsonpath(self.records_jsonpath, input=response.json())
            )
        else:
            yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def get_url(self, context: Context | None) -> str:
        """Get URL for the stream.

        Args:
            context: Stream partition or context dictionary.

        Returns:
            URL for the stream.
        """
        # For profiles stream, the path is dynamic and set in the stream class
        if self.name == "whatconverts_profiles":
            return f"{self.url_base}{self.path}"
        return super().get_url(context)
