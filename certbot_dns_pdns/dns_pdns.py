# SPDX-License-Identifier: Apache-2.0

"""DNS Authenticator for PowerDNS."""

import logging
from collections.abc import Callable
from typing import Any

from certbot import errors
from certbot.plugins import dns_common_lexicon
from requests import HTTPError

logger = logging.getLogger(__name__)


class Authenticator(dns_common_lexicon.LexiconDNSAuthenticator):
    """DNS Authenticator for PowerDNS

    This Authenticator uses the PowerDNS API to fulfill a dns-01 challenge.
    """

    description = (
        "Obtain certificates using a DNS TXT record (if you are using PowerDNS for"
        " DNS)."
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._add_provider_option("endpoint", "PowerDNS API endpoint", "pdns_server")
        self._add_provider_option(
            "api-key",
            "API Key used for authentication with the PowerDNS API",
            "auth_token",
        )
        self._add_provider_option("server-id", "PowerDNS Server ID", "pdns_server_id")
        self._add_provider_option(
            "disable-notify",
            "whether to disable notification of secondaries after record changes",
            "pdns_disable_notify",
        )

    @classmethod
    def add_parser_arguments(
        cls, add: Callable[..., None], default_propagation_seconds: int = 30
    ) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="PowerDNS API credentials INI file.")

    def more_info(self) -> str:
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge"
            " using the PowerDNS API."
        )

    @property
    def _provider_name(self) -> str:
        return "powerdns"

    def _handle_http_error(self, e: HTTPError, domain_name: str) -> errors.PluginError:
        hint = None
        if e.response.status_code == 401:
            hint = "Is your API key correct?"
        if e.response.status_code == 404:
            hint = "Is your server ID correct?"
            if len(domain_name.split(".")) > 1:
                return False

        hint_disp = f" ({hint})" if hint else ""

        return errors.PluginError(
            f"Error determining zone identifier for {domain_name}: '{e}'.{hint_disp}"
        )
