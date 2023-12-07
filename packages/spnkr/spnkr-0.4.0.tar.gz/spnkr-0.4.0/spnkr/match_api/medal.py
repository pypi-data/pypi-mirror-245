from typing import NamedTuple

from ..models import gamecms_hacs
from ..models.refdata import MedalDifficulty, MedalType


class Medal(NamedTuple):
    medal_id: int
    name: str
    description: str
    difficulty: MedalDifficulty
    type: MedalType
    personal_score: int


def create_medal(medal: gamecms_hacs.Medal) -> Medal:
    """Create a Medal from a MedalResponse."""
    return Medal(
        medal_id=medal.name_id,
        name=medal.name.value,
        description=medal.description.value,
        difficulty=medal.difficulty,
        type=medal.type,
        personal_score=medal.personal_score,
    )
