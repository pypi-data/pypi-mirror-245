"""Provides a high-level user interface for accessing Halo Infinite match data."""

import asyncio
import logging
from typing import AsyncIterator, Callable, Iterable, Literal
from uuid import UUID

from aiohttp import ClientResponseError

from ..client import HaloInfiniteClient
from ..models.refdata import LifecycleMode
from ..models.skill import MatchSkill
from ..models.stats import MatchInfo
from . import asset, caching, match, match_info, medal

logger = logging.getLogger(__name__)

_HISTORY_PAGE_SIZE = 25


class HaloInfiniteMatchAPI:
    """A high-level wrapper for `HaloInfiniteClient` to request match data.

    Benefits of using this class over `HaloInfiniteClient` directly include:

    - Caching of response data.
    - Automatic retrieval of map, mode, playlist, skill, and user data when
      requesting a match.
    - A simplified iterator for retrieving a player's match history.
    - Simple, direct data structures for accessing match data.
    """

    def __init__(
        self,
        client: HaloInfiniteClient,
        asset_cache: caching.AssetCache | None = None,
    ) -> None:
        """Initialize a high-level API for requesting Halo Infinite match data.

        Args:
            client: The client to use for API calls.
            asset_cache: The cache to use for asset data. By default, an empty
                cache will be created. However, you can pre-populate a cache
                with data from a previous session by passing in an existing
                cache. This will bypass the need to request some assets from the
                API. You can dump the cache to a file for later use by accessing
                the instance variable `asset_cache`.
        """
        self.client = client
        self.asset_cache = asset_cache or caching.AssetCache()
        self._matches: dict[UUID, match.Match] = {}
        self._medals: dict[int, medal.Medal] | None = None

    async def get_match_history(
        self,
        player: str | int,
        start: int = 0,
        count: int = 25,
        match_type: Literal["all", "matchmaking", "custom", "local"] = "all",
    ) -> list[match_info.MatchInfo]:
        """Get matches in a player's match history, most recent first.

        Args:
            player: Xbox Live ID or gamertag of the player to get counts for.
                Examples of valid inputs include "xuid(1234567890123456)",
                "1234567890123456", 1234567890123456, and "MyGamertag".
            start: Index of the first match to request, starting at 0.
            count: The number of matches to request. Unlike
                `HaloInfiniteClient.get_match_history()`, the value is not
                limited to 25.
            match_type: The type of matches to return. One of "all",
                "matchmaking", "custom", or "local".

        Returns:
            The requested matches.
        """
        n = _HISTORY_PAGE_SIZE
        indices = range(start, start + count, min(count, n))
        tasks = []
        for i in indices:
            n = min(start + count - i, n)
            tasks.append(self._get_history(player, i, n, match_type))
        pages = await asyncio.gather(*tasks)
        return [match for page in pages for match in page]

    async def get_matches(
        self, match_ids: Iterable[str | UUID]
    ) -> list[match.Match]:
        """Get matches by ID.

        Args:
            match_ids: The UUIDs of the matches to request.

        Returns:
            The requested matches.
        """
        tasks = [self.get_match(match_id) for match_id in match_ids]
        return await asyncio.gather(*tasks)

    async def get_match(self, match_id: str | UUID) -> match.Match:
        """Request a match by ID.

        Args:
            match_id: The UUID of the match to request.

        Returns:
            The requested match.
        """
        match_id = UUID(str(match_id))
        if match_id not in self._matches:
            self._matches[match_id] = await self._get_match(match_id)
        return self._matches[match_id]

    async def _get_history(
        self,
        player: str | int,
        start: int,
        count: int,
        match_type: Literal["all", "matchmaking", "custom", "local"],
    ) -> list[match_info.MatchInfo]:
        """Get a page of matches from a player's match history."""
        history = await self.client.stats.get_match_history(
            player, start, count, match_type
        )
        tasks = []
        for r in history.results:
            tasks.append(self._get_match_info(r.match_id, r.match_info))
        return await asyncio.gather(*tasks)

    async def _get_match_info(
        self, match_id: str | UUID, info: MatchInfo
    ) -> match_info.MatchInfo:
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
        return match_info.create_match_info(
            match_id, info, map_, mode, playlist
        )

    async def _get_match(self, match_id: str | UUID) -> match.Match:
        """Request a match by ID."""
        stats = await self.client.stats.get_match_stats(match_id)
        xuids = [p.player_id for p in stats.players if p.is_human]
        if stats.match_info.lifecycle_mode is LifecycleMode.MATCHMADE:
            skill = await self.client.skill.get_match_skill(match_id, xuids)
        else:
            skill = None
        return match.create_match(
            match_stats=stats,
            info=await self._get_match_info(match_id, stats.match_info),
            gamertags=await self._get_gamertags_by_id(xuids),
            match_skill=skill,
            medals=await self._get_medals(),
        )

    # async def _get_skill(
    #     self, match_id: UUID, xuids: list[str]
    # ) -> MatchSkill | None:
    #     """Get skill data for a match and a list of players."""
    #     # TODO - Might be able to skip custom/local matches.
    #     try:
    #         return await self.client.skill.get_match_skill(match_id, xuids)
    #     except ClientResponseError as e:
    #         # "404 Not Found" errors are expected for some matches.
    #         if e.status != 404:
    #             raise
    #         ids = ", ".join(xuids)
    #         logger.warning(
    #             f"No skill data for match '{match_id}' and players {ids}"
    #         )

    async def _get_asset(
        self, getter: Callable, asset_id: UUID, version_id: UUID
    ) -> asset.Asset:
        cached = self.asset_cache.get(asset_id, version_id)
        if cached is not None:
            return cached
        try:
            result = asset.create_asset(await getter(asset_id, version_id))
        except ClientResponseError as e:
            if e.status != 404:
                raise
            logger.warning(f"Asset not found: {e.request_info.url}")
            result = asset.Asset(asset_id, version_id, "404 NOT FOUND", "")
        self.asset_cache.set(result)
        return result

    async def _get_map(self, asset_id: UUID, version_id: UUID) -> asset.Asset:
        getter = self.client.discovery_ugc.get_map
        return await self._get_asset(getter, asset_id, version_id)

    async def _get_mode(self, asset_id: UUID, version_id: UUID) -> asset.Asset:
        getter = self.client.discovery_ugc.get_ugc_game_variant
        return await self._get_asset(getter, asset_id, version_id)

    async def _get_playlist(
        self, asset_id: UUID, version_id: UUID
    ) -> asset.Asset | None:
        getter = self.client.discovery_ugc.get_playlist
        return await self._get_asset(getter, asset_id, version_id)

    async def _get_gamertags_by_id(self, xuids: list[str]) -> dict[int, str]:
        # TODO - Is there a worthwhile way to cache users?
        # TODO - Make sure get_users_by_id handles an empty list.
        users = await self.client.profile.get_users_by_id(xuids)
        return {u.xuid: u.gamertag for u in users}

    async def _get_medals(self) -> dict[int, medal.Medal]:
        if self._medals is None:
            metadata = await self.client.gamecms_hacs.get_medal_metadata()
            self._medals = {
                m.name_id: medal.create_medal(m) for m in metadata.medals
            }
        return self._medals
