"""Karrio Australia Post settings."""

import attr
from karrio.providers.australiapost.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Australia Post connection settings."""

    # Carrier specific properties
    api_key: str
    password: str
    account_number: str

    # Base properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "australiapost"
    account_country_code: str = "AU"
    metadata: dict = {}
    config: dict = {}
