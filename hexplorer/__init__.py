from hexplorer.api.datadragon import DataDragon
from hexplorer.api.lol.champion import ChampionV3
from hexplorer.api.lol.champion_mastery import ChampionMasteryV4
from hexplorer.api.lol.clash import ClashV1
from hexplorer.api.lol.league import LeagueV4
from hexplorer.api.lol.league_exp import LeagueExpV4
from hexplorer.api.lol.match import MatchV5
from hexplorer.api.lol.spectator import SpectatorV4
from hexplorer.api.lol.status import StatusV4
from hexplorer.api.lol.summoner import SummonerV4
from hexplorer.api.riot import Account

__version__ = "0.1.0"


class LolApiDispatch:
    def __init__(self, riot_token: str) -> None:
        self.champion = ChampionV3(riot_token)
        self.champion_mastery = ChampionMasteryV4(riot_token)
        self.clash = ClashV1(riot_token)
        self.league = LeagueV4(riot_token)
        self.league_exp = LeagueExpV4(riot_token)
        self.match = MatchV5(riot_token)
        self.spectator = SpectatorV4(riot_token)
        self.status = StatusV4(riot_token)
        self.summoner = SummonerV4(riot_token)


class RiotApiDispatch:
    def __init__(self, riot_token: str) -> None:
        self.account = Account(riot_token)
        self.lol = LolApiDispatch(riot_token)
        self.ddragon = DataDragon()
