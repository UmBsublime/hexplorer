from typing import List
from loguru import logger

from hexplorer import RiotApiDispatch
from hexplorer.constants import Continent, Region
from hexplorer.config import STDERR_HANDLER, SETTINGS
from hexplorer.persist import PersistanceManager
from hexplorer.models.match_v5 import InfoDto


def main():
    logger.configure(handlers=STDERR_HANDLER)
    logger.disable("hexplorer.api")

    persist = PersistanceManager(SETTINGS.db_url)

    api = RiotApiDispatch(SETTINGS.api_key)

    me = api.lol.summoner.by_name(Region.NA1, "SillyPlays")
    last_matches = api.lol.match.matches_by_puuid(Continent.AMERICAS, me.puuid, count=5)

    for match_id in last_matches:
        if not persist.retreive(match_id, InfoDto):
            logger.info(f"Fetching match {match_id} from api")
            matchdto = api.lol.match.match(Continent.AMERICAS, match_id)
            persist.store(matchdto.info)

    persist.retreive("NA1_00000", InfoDto)


if __name__ == "__main__":
    main()
