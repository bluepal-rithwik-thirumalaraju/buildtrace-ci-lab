from decimal import Decimal

import pytest

from invoice_lab.calculator import calculate_invoice
from invoice_lab.models import InvoiceRequest
from invoice_lab.settings import Settings


@pytest.mark.parametrize(
    ("price", "quantity", "discount", "tax", "expected"),
    [
        ("100.00", 1, "10", "10", ("100.00", "10.00", "9.00", "99.00")),
        ("19.99", 3, "0", "0", ("59.97", "0.00", "0.00", "59.97")),
        ("100.00", 1, "100", "20", ("100.00", "100.00", "0.00", "0.00")),
        ("0.05", 1, "0", "10", ("0.05", "0.00", "0.01", "0.06")),
        ("0.05", 1, "10", "0", ("0.05", "0.01", "0.00", "0.04")),
        ("0.00", 2, "25", "18", ("0.00", "0.00", "0.00", "0.00")),
    ],
)
def test_invoice_amounts(price, quantity, discount, tax, expected):
    order = InvoiceRequest.model_validate(
        {
            "items": [{"name": "Item", "quantity": quantity, "unit_price": price}],
            "discount_percent": discount,
            "tax_percent": tax,
        }
    )
    result = calculate_invoice(order, Settings(currency="USD"))
    assert (result.subtotal, result.discount, result.tax, result.total) == tuple(
        Decimal(value) for value in expected
    )


def test_multiple_items_and_currency():
    order = InvoiceRequest.model_validate(
        {
            "items": [
                {"name": "Keyboard", "quantity": 1, "unit_price": "50.00"},
                {"name": "Mouse", "quantity": 2, "unit_price": "25.00"},
            ],
            "discount_percent": "10",
            "tax_percent": "10",
        }
    )
    assert calculate_invoice(order, Settings(currency="INR")).as_dict() == {
        "currency": "INR",
        "subtotal": "100.00",
        "discount": "10.00",
        "tax": "9.00",
        "total": "99.00",
    }
