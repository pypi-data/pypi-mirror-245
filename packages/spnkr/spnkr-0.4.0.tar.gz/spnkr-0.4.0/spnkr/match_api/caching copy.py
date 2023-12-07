import asyncio
import csv
import io
import os
from uuid import UUID

from aiocache import BaseCache
from aiohttp import ClientSession

from .asset import Asset

ASSET_CSV_URL = ".../assets.csv"


async def load_assets_from_url(
    session: ClientSession, url: str = ASSET_CSV_URL
) -> list[Asset]:
    """Load assets from a CSV file."""
    response = await session.get(url)
    return _load_assets_from_csv(await response.text())


def load_assets_from_file(csv_path: str | os.PathLike) -> list[Asset]:
    """Load assets from a CSV file."""
    with open(csv_path, "r") as f:
        return _load_assets_from_csv(f.read())


async def cache_assets(cache: BaseCache, assets: list[Asset]) -> None:
    """Load assets into the cache."""
    tasks = []
    for asset in assets:
        key = generate_asset_key(asset.asset_id, asset.version_id)
        tasks.append(cache.set(key, asset))
    await asyncio.gather(*tasks)


def generate_asset_key(asset_id: UUID, version_id: UUID) -> str:
    """Generate a cache key for an asset."""
    return f"asset:{asset_id}_{version_id}"


def generate_match_key(match_id: str | UUID) -> str:
    """Generate a cache key for a match."""
    return f"match:{match_id}"


def generate_medals_key() -> str:
    """Generate a cache key for medal metadata."""
    return "medal_metadata"


def _load_assets_from_csv(csv_text: str) -> list[Asset]:
    """Load assets from CSV data."""
    reader = csv.DictReader(io.StringIO(csv_text))
    reader.fieldnames = [f.lower() for f in reader.fieldnames or []]
    if set(reader.fieldnames) < set(Asset.__annotations__):
        raise ValueError(f"Invalid CSV field names: {reader.fieldnames}")

    out = []
    for row in reader:
        asset = Asset(
            asset_id=UUID(row["asset_id"]),
            version_id=UUID(row["version_id"]),
            name=row["name"],
            description=row["description"],
        )
        out.append(asset)
    return out
