from typing import List

from hexplorer.api.riot import LolApi
from hexplorer.constants import Division, Queue, Region, Tier
from hexplorer.models import league_exp_v4


class LeagueExp(LolApi):
    name = "league-exp"


class LeagueExpV4(LeagueExp):
    version = "v4"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, LeagueExp.name, self.version)

    def entries(
        self, region: Region, queue: Queue, tier: Tier, division: Division, page: int = 1
    ) -> List[league_exp_v4.LeagueEntryDTO]:
        return self.get_object(
            region,
            f"entries/{queue.name}/{tier.name}/{division.name}?page={page}",
            league_exp_v4.LeagueEntryDTO,
        )
