from hexplorer.api.riot import LolApi
from hexplorer.constants import Region
from hexplorer.models import lol_status_v3, lol_status_v4


class Status(LolApi):
    name = "status"


class StatusV3(Status):
    version = "v3"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, Status.name, self.version)

    def shard_data(self, region: Region) -> lol_status_v3.ShardStatus:
        return self.get_object(
            region,
            f"shard-data",
            lol_status_v3.ShardStatus,
        )


class StatusV4(Status):
    version = "v4"

    def __init__(self, riot_token: str) -> None:
        super().__init__(riot_token, Status.name, self.version)

    def platform_data(self, region: Region) -> lol_status_v4.PlatformDataDto:
        return self.get_object(
            region,
            f"platform-data",
            lol_status_v4.PlatformDataDto,
        )
