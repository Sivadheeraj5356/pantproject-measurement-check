# Pant Project Measurement Check

A small Python utility for checking custom-pants orders before production or alteration review.

The Pant Project's custom-made flow depends on clean measurements. This checker flags missing fields, implausible values and simple consistency problems across waist, hip, thigh, inseam, outseam and rise, plus fit preference and fabric.

## Run

```bash
python3 measurement_check.py examples/custom_pants_order.json
```

The command prints a JSON report with a 0-100 score, `pass` / `review` / `fail` status, and the exact flags that need attention.

## Test

```bash
python3 -m unittest -v
```

## Input shape

```json
{
  "order_id": "TPP-EXAMPLE-001",
  "fit_preference": "tapered",
  "fabric": "power stretch cotton",
  "measurements_cm": {
    "waist": 82,
    "hip": 98,
    "thigh": 58,
    "inseam": 74,
    "outseam": 102,
    "rise": 27
  }
}
```

No external services or credentials are used.
