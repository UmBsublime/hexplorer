from typing import List

from hexplorer.api.riot import LolApi
from hexplorer.constants import Region
from hexplorer.models import champion_mastery_v4


class ChampionMastery(LolApi):
    name = "champion-mastery"


class ChampionMasteryV4(ChampionMastery):
    version = "v4"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, ChampionMastery.name, self.version)

    def by_summoner(self, region: Region, summoner_id: str) -> List[champion_mastery_v4.ChampionMasteryDto]:
        return self.get_object(
            region, f"champion-masteries/by-summoner/{summoner_id}", champion_mastery_v4.ChampionMasteryDto
        )

    def by_summoner_by_champion(
        self, region: Region, summoner_id: str, champion_id: int
    ) -> champion_mastery_v4.ChampionMasteryDto:
        return self.get_object(
            region,
            f"champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}",
            champion_mastery_v4.ChampionMasteryDto,
        )

    def score_by_summoner(self, region: Region, summoner_id: str) -> int:
        return self.get_object(region, f"scores/by-summoner/{summoner_id}", int)
