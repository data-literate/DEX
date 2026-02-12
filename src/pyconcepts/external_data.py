from __future__ import annotations

from datetime import datetime
from typing import TypedDict

import httpx

COINDESK_ENDPOINT = "https://api.coindesk.com/v1/bpi/currentprice/{currency}.json"


class ExternalDataPoint(TypedDict):
    """Minimal shape returned by the external data helper."""

    symbol: str
    currency: str
    value: float
    timestamp: datetime
    source: str


async def fetch_external_data(currency: str = "USD") -> ExternalDataPoint:
    """Asynchronously fetch a market rate that mirrors the pyconcepts example."""

    currency_code = currency.upper()
    url = COINDESK_ENDPOINT.format(currency=currency_code)

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        payload = response.json()

    rate_info = payload["bpi"].get(currency_code)
    if not rate_info:
        raise ValueError(f"Currency '{currency_code}' not found in payload.")

    timestamp = datetime.fromisoformat(payload["time"]["updatedISO"])
    return ExternalDataPoint(
        symbol="BTC",
        currency=currency_code,
        value=float(rate_info["rate_float"]),
        timestamp=timestamp,
        source=url,
    )
