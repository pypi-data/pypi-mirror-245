import datetime as dt
from typing import NamedTuple, Protocol

from ..models.refdata import GameVariantCategory
from . import asset


class MatchInfo(NamedTuple):
    """Information about a Halo Infinite match."""

    start_time: dt.datetime
    end_time: dt.datetime
    duration: dt.timedelta
    category: GameVariantCategory
    season_id: str | None
    map: asset.Asset
    mode: asset.Asset
    playlist: asset.Asset | None


class _MatchInfoResponse(Protocol):
    """Simplified match info response model."""

    start_time: dt.datetime
    end_time: dt.datetime
    duration: dt.timedelta
    game_variant_category: GameVariantCategory
    season_id: str | None


def create_match_info(
    info: _MatchInfoResponse,
    map_: asset.Asset,
    mode: asset.Asset,
    playlist: asset.Asset | None,
) -> MatchInfo:
    """Combine match info with map, mode, and playlist data."""
    return MatchInfo(
        start_time=info.start_time,
        end_time=info.end_time,
        duration=info.duration,
        category=info.game_variant_category,
        season_id=info.season_id,
        map=map_,
        mode=mode,
        playlist=playlist,
    )
