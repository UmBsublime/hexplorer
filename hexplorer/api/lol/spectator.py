from hexplorer.api.riot import LolApi
from hexplorer.constants import Region
from hexplorer.models import spectator_v4


class Spectator(LolApi):
    name = "spectator"


class SpectatorV4(Spectator):
    version = "v4"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, Spectator.name, self.version)

    def by_summoner(self, region: Region, summoner_id: str) -> spectator_v4.CurrentGameInfo:
        return self.get_object(
            region,
            f"active-games/by-summoner/{summoner_id}",
            spectator_v4.CurrentGameInfo,
        )

    def featured_games(self, region: Region) -> spectator_v4.FeaturedGames:
        return self.get_object(region, "featured-games", spectator_v4.FeaturedGames)
