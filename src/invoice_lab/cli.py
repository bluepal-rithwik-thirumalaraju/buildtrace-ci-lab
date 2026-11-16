"""Read an order and print a machine-readable invoice."""

import argparse
import json
from pathlib import Path

from pydantic import ValidationError

from invoice_lab.calculator import calculate_invoice
from invoice_lab.models import InvoiceRequest
from invoice_lab.settings import ConfigurationError, Settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate an invoice from a JSON order")
    parser.add_argument("order", type=Path, help="Path to the JSON order")
    args = parser.parse_args(argv)
    try:
        settings = Settings.from_environment()
        order = InvoiceRequest.model_validate_json(args.order.read_text(encoding="utf-8"))
        result = calculate_invoice(order, settings)
    except (OSError, UnicodeError, ValidationError, ConfigurationError) as exc:
        parser.exit(2, f"invoice-lab: {exc}\n")
    print(json.dumps(result.as_dict(), indent=2))
    return 0
