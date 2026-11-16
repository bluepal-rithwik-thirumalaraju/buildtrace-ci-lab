"""The input contract for an invoice."""

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

Money = Annotated[
    Decimal,
    Field(ge=0, max_digits=12, decimal_places=2, allow_inf_nan=False),
]
Percentage = Annotated[
    Decimal,
    Field(ge=0, le=100, max_digits=5, decimal_places=2, allow_inf_nan=False),
]


class InvoiceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    quantity: int = Field(gt=0, le=10_000, strict=True)
    unit_price: Money

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class InvoiceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[InvoiceItem] = Field(min_length=1, max_length=1_000)
    discount_percent: Percentage = Decimal("0")
    tax_percent: Percentage = Decimal("0")
