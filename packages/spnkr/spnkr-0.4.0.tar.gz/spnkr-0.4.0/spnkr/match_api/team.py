"""Provides a high-level team model for accessing match data."""

from typing import NamedTuple

from ..models.stats import TeamStats
from . import medal


class Team(NamedTuple):
    team_id: int
    score: int
    kills: int
    deaths: int
    assists: int
    headshot_kills: int
    damage_dealt: int
    damage_taken: int
    medal_counts: tuple[tuple[medal.Medal, int], ...]
    mmr: float | None

    def get_medal_counts_by_name(self) -> dict[str, tuple[medal.Medal, int]]:
        return {mdl.name: (mdl, count) for mdl, count in self.medal_counts}


def create_team(
    team_stats: TeamStats, mmr: float | None, medals: dict[int, medal.Medal]
) -> Team:
    core_stats = team_stats.stats.core_stats
    medal_counts = tuple(
        (medals[award.name_id], award.count) for award in core_stats.medals
    )
    return Team(
        team_id=team_stats.team_id,
        score=core_stats.score,
        kills=core_stats.kills,
        deaths=core_stats.deaths,
        assists=core_stats.assists,
        headshot_kills=core_stats.headshot_kills,
        damage_dealt=core_stats.damage_dealt,
        damage_taken=core_stats.damage_taken,
        medal_counts=medal_counts,
        mmr=mmr,
    )
