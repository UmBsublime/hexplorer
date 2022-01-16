from typing import List, Union

from hexplorer.api.base import Api
from hexplorer.constants import HTTP_method
from hexplorer.models.datadragron_runes import RuneStyleDTO


class DataDragon(Api):
    version = "12.1.1"
    lang = "en_US"
    base_url = "https://ddragon.leagueoflegends.com"
    base_endpoint = f"cdn/{version}/data/{lang}"

    def __init__(self):
        self._runes_reforged = None
        super().__init__()

    def runes_reforged(self) -> List[RuneStyleDTO]:
        if not self._runes_reforged:
            self._runes_reforged = self._request_object(
                self.base_url, HTTP_method.GET, f"runesReforged.json", RuneStyleDTO
            )
        return self._runes_reforged


def perkname_from_id(perks: List[RuneStyleDTO], perk_id: int) -> Union[str, None]:
    for styles in perks:
        for rune_selection in styles.slots:
            for rune in rune_selection.runes:
                if rune.id == perk_id:
                    return rune.name


def perkstyle_from_id(perks: List[RuneStyleDTO], perkstyle_id: int) -> Union[str, None]:
    for style in perks:
        if style.id == perkstyle_id:
            return style.name
