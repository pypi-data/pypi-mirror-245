"""Karrio USPS client settings."""

from karrio.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """USPS connection settings."""

    # Carrier specific properties
    username: str
    password: str
    mailer_id: str = None
    customer_registration_id: str = None
    logistics_manager_mailer_id: str = None

    id: str = None
    account_country_code: str = "US"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "usps"

    @property
    def server_url(self):
        return "https://secure.shippingapis.com/ShippingAPI.dll"

    @property
    def tracking_url(self):
        return "https://tools.usps.com/go/TrackConfirmAction?tLabels={}"
