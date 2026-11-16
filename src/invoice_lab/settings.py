"""Explicit, environment-based application configuration."""

import os
from collections.abc import Mapping
from dataclasses import dataclass

SUPPORTED_CURRENCIES = frozenset({"USD", "EUR", "GBP", "INR"})


class ConfigurationError(ValueError):
    """A required application setting is missing or invalid."""


@dataclass(frozen=True, slots=True)
class Settings:
    currency: str

    def __post_init__(self) -> None:
        currency = self.currency.strip().upper()
        if currency not in SUPPORTED_CURRENCIES:
            supported = ", ".join(sorted(SUPPORTED_CURRENCIES))
            raise ConfigurationError(f"INVOICE_CURRENCY must be one of: {supported}")
        object.__setattr__(self, "currency", currency)

    @classmethod
    def from_environment(cls, environment: Mapping[str, str] | None = None) -> "Settings":
        environment = os.environ if environment is None else environment
        currency = environment.get("INVOICE_CURRENCY", "")
        if not currency.strip():
            raise ConfigurationError("Set INVOICE_CURRENCY before calculating an invoice")
        return cls(currency=currency)
