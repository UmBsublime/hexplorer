from enum import Enum, auto


class Team(Enum):
    Red = 100
    Blue = 200


class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


class Queue(AutoName):
    RANKED_SOLO_5x5 = auto()
    RANKED_TFT = auto()
    RANKED_FLEX_SR = auto()
    RANKED_FLEX_TT = auto()


class HighTier(AutoName):
    CHALLENGER = auto()
    GRANDMASTER = auto()
    MASTER = auto()


class LowTier(AutoName):
    DIAMOND = auto()
    PLATINUM = auto()
    GOLD = auto()
    SILVER = auto()
    BRONZE = auto()
    IRON = auto()


class Tier(AutoName):
    CHALLENGER = auto()
    GRANDMASTER = auto()
    MASTER = auto()
    DIAMOND = auto()
    PLATINUM = auto()
    GOLD = auto()
    SILVER = auto()
    BRONZE = auto()
    IRON = auto()


class Division(AutoName):
    I = auto()
    II = auto()
    III = auto()
    IV = auto()


class ApiRegion(AutoName):
    ...


class Continent(ApiRegion):
    AMERICAS = auto()
    ASIA = auto()
    EUROPE = auto()


class Region(ApiRegion):
    BR1 = auto()
    EUN1 = auto()
    EUW1 = auto()
    JP1 = auto()
    KR = auto()
    LA1 = auto()
    LA2 = auto()
    NA1 = auto()
    OC1 = auto()
    RU = auto()
    TR1 = auto()


class HTTPVerb(AutoName):
    GET = auto()
    PUT = auto()
    POST = auto()
    PATCH = auto()
    DELETE = auto()
    OPTIONS = auto()
    HEAD = auto()
