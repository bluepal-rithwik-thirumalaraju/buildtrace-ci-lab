"""Money calculations use decimal arithmetic and round half up to cents."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from invoice_lab.models import InvoiceRequest
from invoice_lab.settings import Settings

CENT = Decimal("0.01")
HUNDRED = Decimal("100")


def money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True, slots=True)
class InvoiceTotals:
    currency: str
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal

    def as_dict(self) -> dict[str, str]:
        return {
            "currency": self.currency,
            "subtotal": f"{self.subtotal:.2f}",
            "discount": f"{self.discount:.2f}",
            "tax": f"{self.tax:.2f}",
            "total": f"{self.total:.2f}",
        }


def calculate_invoice(order: InvoiceRequest, settings: Settings) -> InvoiceTotals:
    subtotal = money(sum((item.unit_price * item.quantity for item in order.items), Decimal("0")))
    discount = money(subtotal * order.discount_percent / HUNDRED)
    taxable_amount = subtotal - discount
    tax = money(taxable_amount * order.tax_percent / HUNDRED)
    total = money(subtotal + tax)
    return InvoiceTotals(
        currency=settings.currency,
        subtotal=subtotal,
        discount=discount,
        tax=tax,
        total=total,
    )
