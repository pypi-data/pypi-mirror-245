from typing import Callable
from karrio.core import Settings as BaseSettings
from karrio.core.utils import Envelope, apply_namespaceprefix, XP
from karrio.schemas.fedex.rate_service_v28 import (
    WebAuthenticationCredential,
    WebAuthenticationDetail,
    ClientDetail,
)
import karrio.lib as lib


class Settings(BaseSettings):
    """FedEx connection settings."""

    password: str
    meter_number: str
    account_number: str
    user_key: str = None
    language_code: str = "en"
    account_country_code: str = None

    id: str = None
    metadata: dict = {}

    @property
    def server_url(self):
        return (
            "https://wsbeta.fedex.com:443/web-services"
            if self.test_mode
            else "https://ws.fedex.com:443/web-services"
        )

    @property
    def tracking_url(self):
        return "https://www.fedex.com/fedextrack/?trknbr={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.fedex.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def webAuthenticationDetail(self) -> WebAuthenticationDetail:
        return WebAuthenticationDetail(
            UserCredential=WebAuthenticationCredential(
                Key=self.user_key, Password=self.password
            )
        )

    @property
    def clientDetail(self) -> ClientDetail:
        return ClientDetail(
            AccountNumber=self.account_number, MeterNumber=self.meter_number
        )


def default_request_serializer(
    prefix: str, namespace: str
) -> Callable[[Envelope], str]:
    def serializer(envelope: Envelope):
        namespacedef_ = (
            f'xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" {namespace}'
        )

        envelope.Body.ns_prefix_ = envelope.ns_prefix_
        apply_namespaceprefix(envelope.Body.anytypeobjs_[0], prefix)

        return XP.export(envelope, namespacedef_=namespacedef_)

    return serializer
