"""Provides a high-level user interface for accessing Halo Infinite match data."""

import logging
from typing import Any, AsyncIterator, Callable, Literal
from uuid import UUID

from aiohttp import ClientResponseError, ClientSession

from ..client import HaloInfiniteClient
from ..models import stats
from ..models.discovery_ugc import Map, Playlist, UgcGameVariant
from ..models.gamecms_hacs import MedalMetadata
from ..models.skill import MatchSkill
from .match import Match
from .match_info import MatchInfo

__all__ = ["HaloInfiniteMatchAPI"]

logger = logging.getLogger(__name__)


class HaloInfiniteMatchAPI:
    """A high-level API for requesting Halo Infinite match data.

    This API integrates requests using a `HaloInfiniteClient` to provide a
    high-level interface for requesting Halo Infinite match data. When a match
    is requested, map, mode, playlist and skill data will also be requested.
    """

    def __init__(
        self,
        session: ClientSession,
        spartan_token: str,
        clearance_token: str,
        requests_per_second: int | None = 5,
    ) -> None:
        """Initialize a high-level API for requesting Halo Infinite match data.

        Args:
            session: The aiohttp session to use.
            spartan_token: The spartan token used to authenticate with the API.
            clearance_token: The clearance token used to authenticate with the
                API.
            requests_per_second: The rate limit to use. Note that this rate
                limit is enforced per service, not globally. Defaults to 5
                requests per second. Set to None to disable rate limiting.
        """
        self.client = HaloInfiniteClient(
            session, spartan_token, clearance_token, requests_per_second
        )
        # Rather than messing with async caching, store metadata in variables.
        # For the purposes of this class instance, metadata is static.
        # Assets are stored with keys of (asset_id, version_id).
        self._assets: dict[tuple[UUID, UUID], Any] = {}
        self._medal_metadata: MedalMetadata | None = None

    async def iter_match_history(
        self,
        player: str | int,
        start: int = 0,
        count: int | None = None,
        match_type: Literal["all", "matchmaking", "custom", "local"] = "all",
    ) -> AsyncIterator[Match]:
        """Iterate over matches in a player's match history, most recent first.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".
            start: Index of the first match to request, starting at 0.
            count: The number of matches to request. `None` will request all
                available matches.
            match_type: The type of matches to return. One of "all",
                "matchmaking", "custom", or "local".

        Yields:
            The requested matches in order of most recent first.
        """
        remaining = count
        result_count = 25
        while (remaining is None or remaining >= 1) and result_count == 25:
            logger.info(
                f"Retrieving matches {start + 1} to {start + result_count}..."
            )
            history = await self.client.stats.get_match_history(
                player, start, result_count, match_type
            )
            for result in history.results:
                yield await self.get_match(result.match_id)
            result_count += history.result_count
            start += history.result_count
            if remaining is not None:
                remaining -= history.result_count

    async def get_match(self, match_id: str | UUID) -> Match:
        """Request a match by ID.

        Args:
            match_id: The GUID of the match to request.

        Returns:
            The requested match.
        """
        stats = await self.client.stats.get_match_stats(match_id)
        xuids = [p.player_id for p in stats.players if p.is_human]
        return Match(
            _match_stats=stats,
            _info=await self._get_match_info(stats.match_info),
            _users=await self.client.profile.get_users_by_id(xuids),
            _skill=await self._get_skill(stats.match_id, xuids),
            _medal_metadata=await self._get_medal_metadata(),
        )

    async def _get_match_info(self, info: stats.MatchInfo) -> MatchInfo:
        """Combine match info with map, mode, and playlist data."""
        map_ = await self._get_map(
            info.map_variant.asset_id, info.map_variant.version_id
        )
        mode = await self._get_mode(
            info.ugc_game_variant.asset_id, info.ugc_game_variant.version_id
        )
        playlist = None
        if info.playlist is not None:
            playlist = await self._get_playlist(
                info.playlist.asset_id, info.playlist.version_id
            )
        return MatchInfo(info, map_, mode, playlist)

    async def _get_skill(
        self, match_id: UUID, xuids: list[str]
    ) -> MatchSkill | None:
        """Get skill data for a match and a list of players."""
        try:
            return await self.client.skill.get_match_skill(match_id, xuids)
        except ClientResponseError as e:
            if e.status != 404:
                raise
            ids = ", ".join(xuids)
            logger.warning(
                f"No skill data for match '{match_id}' and players {ids}"
            )

    async def _get_asset(
        self, getter: Callable, asset_id: UUID, version_id: UUID
    ):
        """Get an asset by asset ID and version ID."""
        key = (asset_id, version_id)
        if key not in self._assets:
            self._assets[key] = await getter(asset_id, version_id)
        return self._assets[key]

    async def _get_map(self, asset_id: UUID, version_id: UUID) -> Map:
        return await self._get_asset(
            self.client.discovery_ugc.get_map, asset_id, version_id
        )

    async def _get_mode(
        self, asset_id: UUID, version_id: UUID
    ) -> UgcGameVariant:
        return await self._get_asset(
            self.client.discovery_ugc.get_ugc_game_variant, asset_id, version_id
        )

    async def _get_playlist(self, asset_id: UUID, version_id: UUID) -> Playlist:
        return await self._get_asset(
            self.client.discovery_ugc.get_playlist, asset_id, version_id
        )

    async def _get_medal_metadata(self) -> MedalMetadata:
        if self._medal_metadata is None:
            self._medal_metadata = (
                await self.client.gamecms_hacs.get_medal_metadata()
            )
        return self._medal_metadata
