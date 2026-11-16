# BuildTrace CI Lab

A small Python invoice calculator that provides real GitHub Actions inputs for
[BuildTrace](https://github.com/bluepal-rithwik-thirumalaraju/buildtrace).

This repository is the application under test. The debugging agent and its
evidence-linked memory live in the separate BuildTrace repository.

## What the application does

- Validates orders with Pydantic.
- Calculates a subtotal, percentage discount, tax, and final total.
- Uses decimal money arithmetic, rounding half up to two decimal places.
- Applies tax after the discount.
- Reads the required `INVOICE_CURRENCY` setting from the environment.
- Supports USD, EUR, GBP, and INR.

The example order has a subtotal of 100.00, a 10.00 discount, 9.00 tax, and a
99.00 final total.

## Set up locally

Use Python 3.11 or newer. GitHub Actions uses Python 3.12.

```sh
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux / Git Bash with a Unix-style virtual environment
source .venv/bin/activate
```

Install and check the project:

```sh
python -m pip install --editable ".[dev]" --constraint ci/constraints.txt
python -m pip check
python -m pytest
python -m build
```

## Calculate an invoice

```powershell
# Windows PowerShell
$env:INVOICE_CURRENCY = "USD"
python -m invoice_lab examples/order.json
```

```sh
# macOS / Linux / Git Bash
INVOICE_CURRENCY=USD python -m invoice_lab examples/order.json
```

Output:

```json
{
  "currency": "USD",
  "subtotal": "100.00",
  "discount": "10.00",
  "tax": "9.00",
  "total": "99.00"
}
```

## GitHub Actions

The **Invoice CI** workflow runs on pushes, pull requests, and manual dispatches.
It installs the project in a clean virtual environment, checks dependencies,
runs tests, builds the package, and executes the example.

Each run preserves available pytest reports and environment records as an
artifact, even when a test fails. Records include the checked-out commit,
Python version, package versions, and whether the currency setting was present.
Secret environment values are not collected.

Manual runs also accept `source_sha` and `oracle_mode`. BuildTrace uses these to
run the trusted workflow from a pinned healthy revision against an experimental
candidate. Oracle mode fixes pytest discovery and clears extra pytest arguments;
the experiment verifier also requires all 36 original tests, zero skipped tests,
and an environment record proving which candidate was checked out.

The candidate's own CI and this independent oracle must both pass. Each oracle
run is named with its candidate SHA so one trial cannot reuse another trial's
verification result.

## Controlled failures

`main` is the healthy reference application. Separate case branches provide
isolated failing revisions for debugging experiments. Give BuildTrace the
Actions run URL for the exact case you want to investigate.

Scenario recipes, reference repairs, and evaluation instructions belong to the
separate experiment harness, so they are not part of the application snapshot
presented to the debugging agent.
