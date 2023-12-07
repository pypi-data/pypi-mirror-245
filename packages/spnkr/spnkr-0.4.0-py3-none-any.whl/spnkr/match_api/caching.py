import csv
import os
from typing import Iterable, Iterator, TextIO
from uuid import UUID

from .asset import Asset


class AssetCache:
    """A simple dict cache for assets."""

    def __init__(self) -> None:
        self._assets: dict[tuple[UUID, UUID], Asset] = {}

    def get(self, asset_id: UUID, version_id: UUID) -> Asset | None:
        """Get an asset from the cache."""
        return self._assets.get((asset_id, version_id))

    def set(self, asset: Asset) -> None:
        """Set an asset in the cache."""
        self._assets[(asset.asset_id, asset.version_id)] = asset

    def delete(self, asset_id: UUID, version_id: UUID) -> None:
        """Delete an asset from the cache."""
        del self._assets[(asset_id, version_id)]

    def read_csv(self, csv_path: str | os.PathLike) -> None:
        """Load assets from a CSV file."""
        with open(csv_path, "r") as f:
            for asset in _iter_asset_csv(f):
                self.set(asset)

    def to_csv(self, csv_path: str | os.PathLike) -> None:
        """Dump assets to a CSV file."""
        with open(csv_path, "w", newline="") as f:
            _dump_asset_csv(f, self._assets.values())


def _iter_asset_csv(buffer: TextIO) -> Iterator[Asset]:
    """Iterate over assets from CSV data."""
    reader = csv.DictReader(buffer)
    reader.fieldnames = [f.lower() for f in reader.fieldnames or []]
    if set(reader.fieldnames) < set(Asset.__annotations__):
        raise ValueError(f"Invalid CSV field names: {reader.fieldnames}")

    for row in reader:
        yield Asset(
            asset_id=UUID(row["asset_id"]),
            version_id=UUID(row["version_id"]),
            name=row["name"],
            description=row["description"],
        )


def _dump_asset_csv(buffer: TextIO, assets: Iterable[Asset]) -> None:
    """Dump assets to CSV data."""
    writer = csv.DictWriter(
        buffer,
        fieldnames=["asset_id", "version_id", "name", "description"],
        lineterminator="\n",
    )
    writer.writeheader()
    for asset in assets:
        row = {
            "asset_id": asset.asset_id,
            "version_id": asset.version_id,
            "name": asset.name,
            "description": asset.description,
        }
        writer.writerow(row)
