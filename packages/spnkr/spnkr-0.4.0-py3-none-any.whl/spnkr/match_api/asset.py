from typing import NamedTuple, Protocol
from uuid import UUID


class Asset(NamedTuple):
    asset_id: UUID
    version_id: UUID
    name: str
    description: str


class _AssetResponse(Protocol):
    """Simplified asset response model."""

    asset_id: UUID
    version_id: UUID
    public_name: str
    description: str


def create_asset(asset: _AssetResponse) -> Asset:
    return Asset(
        asset_id=asset.asset_id,
        version_id=asset.version_id,
        name=asset.public_name,
        description=asset.description,
    )
