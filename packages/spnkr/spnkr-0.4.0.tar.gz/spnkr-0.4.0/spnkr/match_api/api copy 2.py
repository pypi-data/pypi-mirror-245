"""Provides a high-level user interface for accessing Halo Infinite match data."""

import asyncio
import logging
from typing import AsyncIterator, Callable, Literal
from uuid import UUID

import aiocache
from aiohttp import ClientResponseError

from ..client import HaloInfiniteClient
from ..models.skill import MatchSkill
from ..models.stats import MatchInfo
from . import asset, caching, match, match_info, medal

logger = logging.getLogger(__name__)


class HaloInfiniteMatchAPI:
    """A high-level wrapper for `HaloInfiniteClient` to request match data.

    Benefits of using this class over `HaloInfiniteClient` directly include:

    - Caching of requests.
    - Automatic retrieval of map, mode, playlist, skill, and user data when
      requesting a match.
    - A simplified iterator for retrieving a player's match history.
    - Simple, direct data structures for accessing match data.
    """

    def __init__(self, client: HaloInfiniteClient) -> None:
        """Initialize a high-level API for requesting Halo Infinite match data.

        Args:
            client: The client to use for API calls.
        """
        self.client = client
        self.cache = aiocache.Cache()

    async def iter_match_history(
        self,
        player: str | int,
        start: int = 0,
        count: int | None = None,
        *,
        match_type: Literal["all", "matchmaking", "custom", "local"] = "all",
        match_filter: Callable[[match_info.MatchInfo], bool] | None = None,
    ) -> AsyncIterator[match.Match]:
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
        count = count or int(10e10)
        retrieved = 0
        result_count = 25
        match_filter = match_filter or (lambda _: True)
        while retrieved < count and result_count == 25:
            logger.info(
                f"Retrieving {player} matches {start + 1} to "
                f"{start + result_count}"
            )
            if count is None or match_filter is not None:
                num_to_request = result_count
            else:
                num_to_request = min(result_count, count - retrieved)
            history = await self.client.stats.get_match_history(
                player, start, num_to_request, match_type
            )
            tasks = []
            for result in history.results:
                info = await self._get_match_info(result.match_info)
                if retrieved >= count:
                    break
                print(info.map.name)
                if match_filter(info):
                    tasks.append(self.get_match(result.match_id, info))
                    retrieved += 1

            for match in await asyncio.gather(*tasks):
                yield match

            result_count = history.result_count
            start += history.result_count

    async def get_match(
        self, match_id: str | UUID, info: match_info.MatchInfo
    ) -> match.Match:
        """Request a match by ID.

        Args:
            match_id: The UUID of the match to request.

        Returns:
            The requested match.
        """
        key = caching.generate_match_key(match_id)
        return await self._use_cache(self._get_match, key, match_id, info)

    async def _get_match(
        self, match_id: str | UUID, info: match_info.MatchInfo
    ) -> match.Match:
        """Request a match by ID."""
        stats = await self.client.stats.get_match_stats(match_id)
        xuids = [p.player_id for p in stats.players if p.is_human]
        return match.create_match(
            match_stats=stats,
            info=info,
            gamertags=await self._get_gamertags_by_id(xuids),
            match_skill=await self._get_skill(stats.match_id, xuids),
            medals=await self._get_medals_cached(),
        )

    async def _use_cache(self, method: Callable, key: str, *args):
        """Use the cache to retrieve/store data."""
        cached = await self.cache.get(key)
        if cached is not None:
            return cached
        result = await method(*args)
        await self.cache.set(key, result)
        return result

    async def _get_match_info(self, info: MatchInfo) -> match_info.MatchInfo:
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
        return match_info.create_match_info(info, map_, mode, playlist)

    async def _get_skill(
        self, match_id: UUID, xuids: list[str]
    ) -> MatchSkill | None:
        """Get skill data for a match and a list of players."""
        # TODO - Might be able to skip custom/local matches.
        try:
            return await self.client.skill.get_match_skill(match_id, xuids)
        except ClientResponseError as e:
            # "404 Not Found" errors are expected for some matches.
            if e.status != 404:
                raise
            ids = ", ".join(xuids)
            logger.warning(
                f"No skill data for match '{match_id}' and players {ids}"
            )

    async def _get_asset(
        self, getter: Callable, asset_id: UUID, version_id: UUID
    ) -> asset.Asset:
        async def _get() -> asset.Asset:
            return asset.create_asset(await getter(asset_id, version_id))

        key = caching.generate_asset_key(asset_id, version_id)
        return await self._use_cache(_get, key)

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

    async def _get_medals_cached(self) -> dict[int, medal.Medal]:
        async def _get():
            metadata = await self.client.gamecms_hacs.get_medal_metadata()
            return {m.name_id: medal.create_medal(m) for m in metadata.medals}

        key = caching.generate_medals_key()
        return await self._use_cache(_get, key)


def _prepare_match_predicate(
    maps: list[str] | None,
) -> Callable[[match_info.MatchInfo], bool]:
    """Prepare a filter function for filtering matches by map."""

    def func(info: match_info.MatchInfo) -> bool:
        conditions = [_case_insensitive_in(info.map.name, maps)]
        return all(conditions)

    return func


def _case_insensitive_in(needle: str, haystack: list[str] | None) -> bool:
    """Check if a value is in a list of values, ignoring case."""
    if not haystack:
        return True

    needle = needle.lower().strip()
    print(needle)
    return any(needle == h.lower().strip() for h in haystack)
