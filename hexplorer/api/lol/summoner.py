from hexplorer.api.riot import LolApi
from hexplorer.constants import Region
from hexplorer.models import summoner_v4


class Summoner(LolApi):
    name = "summoner"


class SummonerV4(Summoner):
    version = "v4"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, Summoner.name, self.version)

    def by_account(self, region: Region, account_id: str) -> summoner_v4.SummonerDTO:
        return self.get_object(region, f"summoners/by-account/{account_id}", summoner_v4.SummonerDTO)

    def by_name(self, region: Region, name: str) -> summoner_v4.SummonerDTO:
        return self.get_object(region, f"summoners/by-name/{name}", summoner_v4.SummonerDTO)

    def by_puuid(self, region: Region, puuid: str) -> summoner_v4.SummonerDTO:
        return self.get_object(region, f"summoners/by-puuid/{puuid}", summoner_v4.SummonerDTO)

    def summoners(self, region: Region, summoner_id: str) -> summoner_v4.SummonerDTO:
        return self.get_object(region, f"summoners/{summoner_id}", summoner_v4.SummonerDTO)

    def me(self, region: Region) -> summoner_v4.SummonerDTO:
        return self.get_object(region, f"summoners/me", summoner_v4.SummonerDTO)
