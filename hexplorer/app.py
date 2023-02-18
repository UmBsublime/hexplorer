from loguru import logger

from hexplorer import RiotApiDispatch, glue
from hexplorer.api.exceptions import ApiResourceNotFoundError
from hexplorer.config import SETTINGS, STDERR_HANDLER
from hexplorer.constants import (Continent, Division, LowTier, Queue, Region,
                                 Tier)


#@logger.catch
def main():
    logger.configure(handlers=STDERR_HANDLER)

    logger.info("Hello World!")
    riot_api = RiotApiDispatch(SETTINGS.api_key)

    me = riot_api.lol.summoner.by_name(Region.NA1, "SillyPlays")

    # Application token can't access (403)
    # riot_api.account.by_puuid(Continent.AMERICAS, me.puuid)
    # riot_api.account.by_riot_id(Continent.AMERICAS, me.name, Region.NA1)
    
    riot_api.lol.champion.rotations(Region.NA1)

    riot_api.lol.champion_mastery.by_summoner(Region.NA1, me.id)
    riot_api.lol.champion_mastery.by_summoner_by_champion(Region.NA1, me.id, 22)
    riot_api.lol.champion_mastery.score_by_summoner(Region.NA1, me.id)

    riot_api.lol.clash.by_summoner(Region.NA1, me.id)
    tournaments = riot_api.lol.clash.tournaments(Region.NA1)
    if tournaments:
        riot_api.lol.clash.tournaments_by_id(Region.NA1, tournaments[0].id)
    # No teamId to test these
    # riot_api.lol.clash.teams(Region.NA1, 123456)
    # riot_api.lol.clash.tournaments_by_team(Region.NA1, 123456)

    riot_api.lol.league.entries(Region.NA1, Queue.RANKED_SOLO_5x5, LowTier.DIAMOND, Division.I)
    riot_api.lol.league.entries_by_summoner(Region.NA1, me.id)
    riot_api.lol.league.grandmaster_by_queue(Region.NA1, Queue.RANKED_SOLO_5x5)
    riot_api.lol.league.master_by_queue(Region.NA1, Queue.RANKED_SOLO_5x5)
    riot_api.lol.league.challenger_by_queue(Region.NA1, Queue.RANKED_SOLO_5x5)

    riot_api.lol.league_exp.entries(Region.NA1, Queue.RANKED_SOLO_5x5, Tier.CHALLENGER, Division.I)

    try:
        riot_api.lol.spectator.by_summoner(Region.NA1, me.id)
    except ApiResourceNotFoundError:
        ...  # No active game

    riot_api.lol.spectator.featured_games(Region.NA1)

    riot_api.lol.status.platform_data(Region.NA1)

    riot_api.lol.summoner.by_puuid(Region.NA1, me.puuid)
    riot_api.lol.summoner.by_name(Region.NA1, me.name)
    riot_api.lol.summoner.by_account(Region.NA1, me.accountId)
    riot_api.lol.summoner.summoners(Region.NA1, me.id)
    # Application token can't access (403)
    # riot_api.lol.summoner.me(Region.NA1)
    
    last_games = riot_api.lol.match.matches_by_puuid(Continent.AMERICAS, me.puuid, count=1)
    #for match_id in last_games:
    #    riot_api.lol.match.match(Continent.AMERICAS, match_id)
    
    match = riot_api.lol.match.match(Continent.AMERICAS, last_games[0])
    glue.print_match(match)
    # glue.top_five(riot_api.lol, [Region.NA1], Queue.RANKED_SOLO_5x5, Tier.CHALLENGER, Division.I)
    # glue.print_runes()
    # glue.find_active_game(riot_api.lol, SETTINGS.summoner_name)


if __name__ == "__main__":
    main()
