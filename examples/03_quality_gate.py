#!/usr/bin/env python
"""03_quality_gate.py — Data quality gate with live metrics.

Demonstrates:
- ``QualityGate`` evaluating records against medallion layer thresholds
- ``QualityStore`` accumulating per-layer quality history
- Per-dimension quality scores (completeness, accuracy, etc.)
- Pass/fail decisions based on layer configuration

Uses generic product-inventory data with custom required fields.

Run:
    uv run python examples/03_quality_gate.py
"""

from __future__ import annotations

from typing import Any

from dataenginex.core.medallion_architecture import DataLayer
from dataenginex.core.quality import QualityGate, QualityStore

# Required fields for our product-inventory domain
REQUIRED_FIELDS: set[str] = {"product_id", "name", "category", "price"}


def _good_records(count: int = 10) -> list[dict[str, Any]]:
    """High-quality product records — all required fields present."""
    products = [
        ("Wireless Mouse", "Electronics", 29.99, 150),
        ("USB-C Hub", "Electronics", 49.99, 85),
        ("Standing Desk", "Furniture", 399.00, 22),
        ("Mechanical Keyboard", "Electronics", 89.99, 64),
        ("Monitor Arm", "Furniture", 34.99, 200),
        ("Webcam HD", "Electronics", 59.99, 110),
        ("Desk Lamp", "Lighting", 24.99, 300),
        ("Ergonomic Chair", "Furniture", 549.00, 15),
        ("Noise-Cancelling Headphones", "Electronics", 199.99, 45),
        ("Cable Management Kit", "Accessories", 12.99, 500),
    ]
    return [
        {
            "product_id": f"PROD-{1000 + i}",
            "name": products[i % len(products)][0],
            "category": products[i % len(products)][1],
            "price": products[i % len(products)][2],
            "stock": products[i % len(products)][3],
            "supplier": f"Supplier-{i % 3}",
        }
        for i in range(count)
    ]


def _sparse_records(count: int = 5) -> list[dict[str, Any]]:
    """Low-quality records — missing most required fields."""
    return [{"product_id": f"PROD-{9000 + i}"} for i in range(count)]


def main() -> None:
    store = QualityStore()
    gate = QualityGate(store=store)

    # ----- 1. Evaluate good data against each layer -----------------------
    print("=== Complete product data ===")
    for layer in (DataLayer.BRONZE, DataLayer.SILVER, DataLayer.GOLD):
        result = gate.evaluate(
            _good_records(),
            layer=layer,
            required_fields=REQUIRED_FIELDS,
            dataset_name="products_complete",
        )
        status = "PASS ✓" if result.passed else "FAIL ✗"
        print(
            f"  {layer.value:>6}: score={result.quality_score:.4f}  "
            f"threshold={result.threshold:.2f}  {status}"
        )

    # ----- 2. Evaluate sparse data ----------------------------------------
    print("\n=== Sparse product data ===")
    for layer in (DataLayer.BRONZE, DataLayer.SILVER, DataLayer.GOLD):
        result = gate.evaluate(
            _sparse_records(),
            layer=layer,
            required_fields=REQUIRED_FIELDS,
            dataset_name="products_sparse",
        )
        status = "PASS ✓" if result.passed else "FAIL ✗"
        print(
            f"  {layer.value:>6}: score={result.quality_score:.4f}  "
            f"threshold={result.threshold:.2f}  {status}"
        )

    # ----- 3. Check the quality store summary -----------------------------
    print("\n=== Quality store summary ===")
    summary = store.summary()
    print(f"  Overall score: {summary['overall_score']:.4f}")
    print(f"  Layer scores:  {summary['layer_scores']}")
    print(f"  Dimensions:    {summary['dimensions']}")

    # ----- 4. Per-dimension breakdown of the last gold evaluation ----------
    latest_gold = store.latest("gold")
    if latest_gold:
        print("\n=== Latest gold evaluation ===")
        print(f"  Passed: {latest_gold.passed}")
        print(f"  Records: {latest_gold.record_count}")
        for dim, val in latest_gold.dimensions.items():
            print(f"    {dim}: {val:.4f}")

    print("\nDone! ✓")


if __name__ == "__main__":
    main()
