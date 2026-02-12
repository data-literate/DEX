from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from datetime import datetime
from random import uniform

METRIC_TRACKERS: tuple[tuple[str, str], ...] = (
    ("request_rate", "Rolling requests per minute"),
    ("error_rate", "5xx error ratio over the last window"),
    ("in_flight", "Concurrent requests currently in process"),
)


async def insight_stream(
    count: int = 5, interval: float = 0.75
) -> AsyncIterator[dict[str, str | float]]:
    """Stream synthetic insight updates inspired by generators."""

    for index in range(count):
        metric, description = METRIC_TRACKERS[index % len(METRIC_TRACKERS)]
        updated_at = datetime.utcnow().isoformat() + "Z"
        value = round(uniform(0.5, 1.5) * (index + 1), 2)

        yield {
            "metric": metric,
            "value": value,
            "description": description,
            "timestamp": updated_at,
            "source": "pyconcepts.insights",
        }

        await asyncio.sleep(interval)
