import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "order.json"


def run_invoice(path, currency="USD"):
    environment = os.environ.copy()
    environment.pop("INVOICE_CURRENCY", None)
    if currency is not None:
        environment["INVOICE_CURRENCY"] = currency
    return subprocess.run(
        [sys.executable, "-m", "invoice_lab", str(path)],
        env=environment,
        capture_output=True,
        text=True,
        timeout=15,
    )


def test_example_order():
    result = run_invoice(EXAMPLE)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "currency": "USD",
        "subtotal": "100.00",
        "discount": "10.00",
        "tax": "9.00",
        "total": "99.00",
    }


def test_missing_configuration_has_actionable_error():
    result = run_invoice(EXAMPLE, currency=None)
    assert result.returncode == 2
    assert "Set INVOICE_CURRENCY" in result.stderr
    assert not result.stdout


@pytest.mark.parametrize("contents", ["not json", '{"items": []}'])
def test_invalid_order_exits_unsuccessfully(tmp_path, contents):
    order = tmp_path / "order.json"
    order.write_text(contents, encoding="utf-8")
    result = run_invoice(order)
    assert result.returncode == 2
    assert "validation error" in result.stderr


def test_missing_order_exits_unsuccessfully(tmp_path):
    result = run_invoice(tmp_path / "missing.json")
    assert result.returncode == 2
    assert "missing.json" in result.stderr
