import pytest

from invoice_lab.settings import ConfigurationError, Settings


@pytest.mark.parametrize("currency", ["USD", "EUR", "GBP", "INR", " usd "])
def test_currency_is_loaded_from_environment(currency):
    assert Settings.from_environment({"INVOICE_CURRENCY": currency}).currency == currency.strip().upper()


@pytest.mark.parametrize("environment", [{}, {"INVOICE_CURRENCY": ""}, {"INVOICE_CURRENCY": "   "}])
def test_currency_is_required(environment):
    with pytest.raises(ConfigurationError, match="Set INVOICE_CURRENCY"):
        Settings.from_environment(environment)


def test_unsupported_currency_is_rejected():
    with pytest.raises(ConfigurationError, match="must be one of"):
        Settings.from_environment({"INVOICE_CURRENCY": "INVALID"})
