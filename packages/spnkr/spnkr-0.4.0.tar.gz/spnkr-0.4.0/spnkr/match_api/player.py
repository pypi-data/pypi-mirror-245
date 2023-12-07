"""Provides a high-level player model for accessing match data."""

from typing import NamedTuple

from ..models.skill import MatchSkillResult
from ..models.stats import PlayerStats
from . import medal


class Player(NamedTuple):
    player_id: str
    gamertag: str
    is_human: bool
    team_id: int
    score: int
    kills: int
    deaths: int
    assists: int
    headshot_kills: int
    damage_dealt: int
    damage_taken: int
    medal_counts: tuple[tuple[medal.Medal, int], ...]
    csr_before: int | None
    csr_after: int | None
    expected_kills: float | None
    expected_deaths: float | None

    def get_medal_counts_by_name(self) -> dict[str, tuple[medal.Medal, int]]:
        return {mdl.name: (mdl, count) for mdl, count in self.medal_counts}


def create_player(
    player_stats: PlayerStats,
    player_team_index: int,
    gamertag: str,
    skill: MatchSkillResult | None,
    medals: dict[int, medal.Medal],
) -> Player:
    player_team_stats = player_stats.player_team_stats[player_team_index]
    core_stats = player_team_stats.stats.core_stats
    csr_before = csr_after = expected_kills = expected_deaths = None
    if skill:
        csr_before = skill.rank_recap.pre_match_csr.value
        csr_after = skill.rank_recap.post_match_csr.value
        expected_kills = skill.stat_performances.kills.expected
        expected_deaths = skill.stat_performances.deaths.expected
    medal_counts = tuple(
        (medals[award.name_id], award.count) for award in core_stats.medals
    )
    return Player(
        player_id=player_stats.player_id,
        gamertag=gamertag,
        is_human=player_stats.is_human,
        team_id=player_team_stats.team_id,
        score=core_stats.score,
        kills=core_stats.kills,
        deaths=core_stats.deaths,
        assists=core_stats.assists,
        headshot_kills=core_stats.headshot_kills,
        damage_dealt=core_stats.damage_dealt,
        damage_taken=core_stats.damage_taken,
        medal_counts=medal_counts,
        csr_before=csr_before,
        csr_after=csr_after,
        expected_kills=expected_kills,
        expected_deaths=expected_deaths,
    )
