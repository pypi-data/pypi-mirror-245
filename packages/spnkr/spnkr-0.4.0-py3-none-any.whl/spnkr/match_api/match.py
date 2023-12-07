"""Provides a high-level match model for accessing match data."""

from typing import NamedTuple
from uuid import UUID

from ..models.skill import MatchSkill, MatchSkillResult
from ..models.stats import MatchStats, PlayerStats, TeamStats
from ..tools import BOT_MAP
from ..xuid import unwrap_xuid
from . import match_info, medal, player, team


class Match(NamedTuple):
    match_id: UUID
    info: match_info.MatchInfo
    teams: tuple[team.Team, ...]
    players: tuple[player.Player, ...]


def create_match(
    match_stats: MatchStats,
    info: match_info.MatchInfo,
    gamertags: dict[int, str],
    match_skill: MatchSkill | None,
    medals: dict[int, medal.Medal],
) -> Match:
    team_mmrs = match_skill.get_team_mmrs() if match_skill else {}
    skill_results = match_skill.get_results_by_id() if match_skill else {}
    return Match(
        match_id=match_stats.match_id,
        info=info,
        teams=_create_teams(match_stats.teams, team_mmrs, medals),
        players=_create_players(
            match_stats.players, gamertags, skill_results, medals
        ),
    )


def _create_teams(
    teams: list[TeamStats],
    team_mmrs: dict[int, float],
    medals: dict[int, medal.Medal],
) -> tuple[team.Team, ...]:
    return tuple(
        team.create_team(t, team_mmrs.get(t.team_id), medals) for t in teams
    )


def _create_players(
    players: list[PlayerStats],
    gamertags: dict[int, str],
    skill_results: dict[str, MatchSkillResult],
    medals: dict[int, medal.Medal],
) -> tuple[player.Player, ...]:
    out = []
    for p in players:
        if p.is_human:
            xuid = unwrap_xuid(p.player_id)
            name = gamertags.get(xuid, p.player_id)
            skill = skill_results.get(p.player_id)
        else:
            name = BOT_MAP.get(p.player_id, p.player_id)
            skill = None

        for i in range(len(p.player_team_stats)):
            out.append(player.create_player(p, i, name, skill, medals))
    return tuple(out)
