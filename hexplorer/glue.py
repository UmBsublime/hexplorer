from typing import List

from hexplorer import LolApiDispatch
from hexplorer.api.datadragon import DataDragon, perkstyle_from_id
from hexplorer.api.exceptions import ApiFailledToGetResponse
from hexplorer.constants import Division, Queue, Region, Team, Tier
from hexplorer.models.match_v5 import MatchDto

ddragon = DataDragon()


def print_runes() -> None:
    all_runes = ddragon.runes_reforged()
    for runeTree in all_runes:
        print(runeTree.name)
        for rune_line in runeTree.slots:
            print(f"\t{[rune.name for rune in rune_line.runes]}")


def print_match(match: MatchDto) -> None:
    for c, p in enumerate(match.info.participants):
        player_info = f"{Team(p.teamId).name:5}" f"{p.teamPosition:8}" f"{p.summonerName:18}" f"{p.championName:10}"
        kda = (
            f"{p.kills:3}"
            f"{p.deaths:3}"
            f"{p.assists:3}"
            f"{(p.kills+p.assists)/(1 if not p.deaths else p.deaths):6.2f}"
        )
        res = (
            f"{player_info}"
            f"{kda}"
            f"{p.totalDamageDealt:8.0f}"
            f"{' First blood' if p.firstBloodKill else '':14}"
            f"{perkstyle_from_id(ddragon.runes_reforged(), p.perks.styles[0].style):12}"
            f"{perkstyle_from_id(ddragon.runes_reforged(), p.perks.styles[1].style)}"
        )

        print(res)
        if c + 1 == len(match.info.participants) / 2:
            print("---")
    print("---")

    print(
        f"Game was won by {Team.Blue.name if match.info.participants[-1].win else Team.Red.name } team in {match.info.gameDuration/60:.1f}m"
    )


def top_five(lol_api: LolApiDispatch, regions: List[Region], queue: Queue, tier: Tier, division: Division) -> None:
    for region in regions:
        top_players = sorted(
            lol_api.league_exp.entries(region, queue, tier, division), key=lambda x: x.leaguePoints, reverse=True
        )
        print(f"{region.name} {queue.name} {tier.name} {division.name}")
        for player in top_players[:5]:
            print(f"{player.summonerName:18}{player.leaguePoints}")


def find_active_game(lol_api: LolApiDispatch, summoner_name: str) -> None:
    try:
        print(lol_api.spectator.by_summoner(Region.NA1, lol_api.summoner.by_name(Region.NA1, summoner_name).id))
    except ApiFailledToGetResponse:
        print("No active game")
