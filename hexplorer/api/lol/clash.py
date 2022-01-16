from typing import List

from hexplorer.api.riot import LolApi
from hexplorer.constants import Region
from hexplorer.models import clash_v1


# /lol/clash/v1/players/by-summoner/{summonerId}
class Clash(LolApi):
    name = "clash"


class ClashV1(Clash):
    version = "v1"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, Clash.name, self.version)

    def by_summoner(self, region: Region, summoner_id: str) -> List[clash_v1.PlayerDto]:
        return self.get_object(region, f"players/by-summoner/{summoner_id}", clash_v1.PlayerDto)

    def teams(self, region: Region, team_id: str) -> clash_v1.TeamDto:
        return self.get_object(region, f"teams/{team_id}", clash_v1.TeamDto)

    def tournaments(self, region: Region) -> List[clash_v1.TournamentDto]:
        return self.get_object(region, f"tournaments", clash_v1.TournamentDto)

    def tournaments_by_team(self, region: Region, team_id: str) -> clash_v1.TournamentDto:
        return self.get_object(region, f"tournaments/by-team/{team_id}", clash_v1.TournamentDto)

    def tournaments_by_id(self, region: Region, tournament_id: int) -> clash_v1.TournamentDto:
        return self.get_object(region, f"tournaments/{tournament_id}", clash_v1.TournamentDto)
