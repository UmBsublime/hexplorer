from typing import List

from hexplorer.api.riot import LolApi
from hexplorer.constants import Division, LowTier, Queue, Region
from hexplorer.models import league_v4


class League(LolApi):
    name = "league"


class LeagueV4(League):
    version = "v4"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, League.name, self.version)
        self.base_endpoint = f"{self.api}/league/{self.version}"

    def challenger_by_queue(self, region: Region, queue: Queue) -> league_v4.LeagueListDTO:
        return self.get_object(
            region,
            f"challengerleagues/by-queue/{queue.name}",
            league_v4.LeagueListDTO,
        )

    def entries_by_summoner(self, region: Region, summoner_id: str) -> List[league_v4.LeagueEntryDTO]:
        return self.get_object(
            region,
            f"entries/by-summoner/{summoner_id}",
            league_v4.LeagueEntryDTO,
        )

    def entries(
        self, region: Region, queue: Queue, tier: LowTier, division: Division, page: int = 1
    ) -> List[league_v4.LeagueEntryDTO]:
        return self.get_object(
            region,
            f"entries/{queue.name}/{tier.name}/{division.name}?page={page}",
            league_v4.LeagueEntryDTO,
        )

    def grandmaster_by_queue(self, region: Region, queue: Queue) -> league_v4.LeagueListDTO:
        return self.get_object(
            region,
            f"grandmasterleagues/by-queue/{queue.name}",
            league_v4.LeagueListDTO,
        )

    def leagues(self, region: Region, league_id: str) -> league_v4.LeagueListDTO:
        return self.get_object(
            region,
            f"leagues/{league_id}",
            league_v4.LeagueListDTO,
        )

    def master_by_queue(self, region: Region, queue: Queue) -> league_v4.LeagueListDTO:
        return self.get_object(
            region,
            f"masterleagues/by-queue/{queue.name}",
            league_v4.LeagueListDTO,
        )
