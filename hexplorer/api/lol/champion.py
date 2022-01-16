from functools import lru_cache

from hexplorer.api.riot import LolApi
from hexplorer.constants import Region
from hexplorer.models import champion_v3


class Champion(LolApi):
    name = "platform"


class ChampionV3(Champion):
    version = "v3"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, Champion.name, self.version)

    @lru_cache
    def rotations(self, region: Region) -> champion_v3.ChampionInfo:
        return self.get_object(
            region,
            f"champion-rotations",
            champion_v3.ChampionInfo,
        )
