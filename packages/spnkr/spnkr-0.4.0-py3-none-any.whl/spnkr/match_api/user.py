import urllib.parse
from typing import Literal, NamedTuple

from ..models import profile


class User(NamedTuple):
    xuid: int
    gamertag: str
    gamerpic_url: str

    def get_gamerpic_url_as(
        self, size: Literal["64x64", "208x208", "424x424", "1080x1080"]
    ) -> str:
        """Get the URL to the user's gamerpic at a specific size.

        Args:
            size: The size of the gamerpic URL to generate, in pixels. One of
                "64x64", "208x208", "424x424", or "1080x1080".
        """
        result = urllib.parse.urlparse(self.gamerpic_url)
        params = urllib.parse.parse_qs(result.query)
        width, height = size.split("x")
        params["w"] = [width]
        params["h"] = [height]
        return result._replace(query=urllib.parse.urlencode(params)).geturl()


def create_user(profile: profile.User) -> User:
    return User(
        xuid=profile.xuid,
        gamertag=profile.gamertag,
        gamerpic_url=profile.gamerpic.xlarge,
    )
