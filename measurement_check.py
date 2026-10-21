#!/usr/bin/env python3
"""Check a custom pants measurement set for completeness and alteration risk."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

LIMITS_CM = {
    "waist": (55.0, 180.0),
    "hip": (70.0, 190.0),
    "thigh": (35.0, 120.0),
    "inseam": (45.0, 115.0),
    "outseam": (70.0, 135.0),
    "rise": (18.0, 50.0),
}


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def check_measurements(order: dict[str, Any]) -> dict[str, Any]:
    measurements = order.get("measurements_cm")
    if not isinstance(measurements, dict):
        return {"status": "fail", "score": 0, "flags": ["measurements_cm must be an object"]}

    flags: list[str] = []
    for field, (low, high) in LIMITS_CM.items():
        value = _number(measurements.get(field))
        if value is None:
            flags.append(f"missing or invalid {field}")
        elif not low <= value <= high:
            flags.append(f"{field} outside review range {low:g}-{high:g} cm")

    waist = _number(measurements.get("waist"))
    hip = _number(measurements.get("hip"))
    inseam = _number(measurements.get("inseam"))
    outseam = _number(measurements.get("outseam"))
    rise = _number(measurements.get("rise"))

    if waist is not None and hip is not None and hip < waist * 0.9:
        flags.append("hip looks unusually small relative to waist")
    if inseam is not None and outseam is not None and inseam >= outseam:
        flags.append("inseam must be shorter than outseam")
    if rise is not None and outseam is not None and rise >= outseam * 0.55:
        flags.append("rise looks too long relative to outseam")
    if not order.get("fit_preference"):
        flags.append("missing fit preference")
    if not order.get("fabric"):
        flags.append("missing fabric")

    score = max(0, 100 - len(flags) * 15)
    status = "pass" if not flags else "review" if score >= 55 else "fail"
    return {"status": status, "score": score, "flags": flags}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("order_json", type=Path, help="Path to one custom-pants order JSON file")
    args = parser.parse_args()
    order = json.loads(args.order_json.read_text(encoding="utf-8"))
    print(json.dumps(check_measurements(order), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
