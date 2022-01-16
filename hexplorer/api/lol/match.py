from typing import List

from hexplorer.api.riot import LolApi
from hexplorer.constants import Continent
from hexplorer.models import match_v5


class Match(LolApi):
    name = "match"


class MatchV5(Match):
    version = "v5"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, Match.name, self.version)

    def match(self, continent: Continent, match_id: str) -> match_v5.MatchDto:
        return self.get_object(continent, f"matches/{match_id}", match_v5.MatchDto)

    def match_timeline(self, continent: Continent, match_id: str) -> match_v5.MatchTimelineDto:
        return self.get_object(continent, f"matches/{match_id}/timeline", match_v5.MatchTimelineDto)

    def matches_by_puuid(self, continent: Continent, puuid: str, count: int = 20) -> List[str]:
        return self.get_object(continent, f"matches/by-puuid/{puuid}/ids?count={count}", list)
