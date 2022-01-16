from typing import Any

from hexplorer.api.base import Api
from hexplorer.constants import ApiRegion, Continent, HTTP_method, Region
from hexplorer.models import account_v1


class RiotApi(Api):
    api = "riot"

    def __init__(self, riot_token: str, name: str, version: str):
        self.base_url = "https://{}.api.riotgames.com"
        self.session.headers.update({"X-Riot-Token": riot_token})
        self.base_endpoint = f"{self.api}/{name}/{version}"
        super().__init__()

    def __gen_api_region_url(self, region: ApiRegion) -> str:
        return self.base_url.format(region.name.lower())

    def get_object(self, region: ApiRegion, endpoint: str, obj: Any) -> Any:
        return self._request_object(self.__gen_api_region_url(region), HTTP_method.GET, endpoint, obj)


class LolApi(RiotApi):
    api = "lol"


class Account(RiotApi):
    name = "account"
    version = "v1"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, self.name, self.version)

    def by_puuid(self, continent: Continent, puuid: str) -> account_v1.AccountDto:
        return self.get_object(continent, f"accounts/by-puuid/{puuid}", account_v1.AccountDto)

    def by_riot_id(self, continent: Continent, account_name: str, region: Region) -> account_v1.AccountDto:
        return self.get_object(
            continent,
            f"accounts/by-riot-id/{account_name}/{region.name}",
            account_v1.AccountDto,
        )
