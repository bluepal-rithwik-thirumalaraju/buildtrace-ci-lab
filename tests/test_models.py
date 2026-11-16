import pytest
from pydantic import ValidationError

from invoice_lab.models import InvoiceItem, InvoiceRequest


@pytest.mark.parametrize(
    "changes",
    [
        {"name": "   "},
        {"quantity": 0},
        {"quantity": -1},
        {"quantity": True},
        {"quantity": "2"},
        {"unit_price": "-0.01"},
        {"unit_price": "1.001"},
        {"unit_price": "NaN"},
        {"unexpected": "value"},
    ],
)
def test_invalid_items_are_rejected(changes):
    item = {"name": "Item", "quantity": 1, "unit_price": "10.00"}
    with pytest.raises(ValidationError):
        InvoiceItem.model_validate(item | changes)


@pytest.mark.parametrize(
    "changes",
    [
        {"items": []},
        {"discount_percent": "-1"},
        {"discount_percent": "100.01"},
        {"tax_percent": "101"},
        {"tax_percent": "Infinity"},
        {"currency": "USD"},
    ],
)
def test_invalid_orders_are_rejected(changes):
    order = {"items": [{"name": "Item", "quantity": 1, "unit_price": "10.00"}]}
    with pytest.raises(ValidationError):
        InvoiceRequest.model_validate(order | changes)
