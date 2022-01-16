# Hexplorer - WIP

Hexplorer aims to be a simple module to interact with the [League of Legends developer APIs](https://developer.riotgames.com/).

## Features

- All api responses are modeled as pydantic objects thanks to [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) and [riotapi-schema](https://github.com/MingweiSamuel/riotapi-schema)
- Readable and configurable logging thanks to [loguru](https://github.com/Delgan/loguru)
- Configuration as code, with environment variables or with a `.env` file.

## Not Implemented (yet..?)

- Any sort of rate-limiting
- CLI to interact with every api endpoint
- Helper functions to parse and present data
- Documentation aside from this readme (the code is mostly verbose though)
- Unit tests

## Api Support

The following APIs are fully supported

- champion-mastery-v4
- clash-v1
- league-v4
- league-exp-v4
- math-v5
- spectator-v4
- status-v4
- summoner-v4

Datadragon support is very basic at the moment

- runesReforged

## 

## Usage

```python
from hexplorer import RiotApiDispatch
from hexplorer.config import Settings
from hexplorer.constants import Continent, Division, Queue, Region, Tier

settings = Setings(api_key='RGAPI-123code')
riot_api = RiotApiDispatch(settings.api_key)

me = riot_api.lol.summoner.by_name(Region.NA1, 'SillyPlays')

# Get top players for every region
top_players = [riot_api.lol.league_exp.entries(region, Queue.RANKED_SOLO_5x5, Tier.CHALLENGER, Division.I) for region in Region]

# Look for an active game
try:
    riot_api.lol.spectator.by_summoner(Region.NA1, me.id)
except ApiResourceNotFoundError:
    ...  # No active game

# Get last 5 games
last5_id = riot_api.lol.match.matches_by_puuid(Continent.AMERICAS, me.puuid, count=5)
last5_matches = [riot_api.lol.match.match(Continent.AMERICAS, match_id) for match_id in last5_ids]
```

## Configuration

### Settings 


**As code**

```python
from hexplorer.config import Settings

settings = Settings(api_key="RGAPI-123code")
```

When using `.env` or environment variables

```python
from hexplorer import RiotApiDispatch
from hexplorer.config import SETTINGS

riot_api = RiotApiDispatch(SETTINGS.api_key)
```

**Using envorionment variables**

```
export API_KEY="RGAPI-123code" 
```

**Using .env file**

```
API_KEY="RGAPI-123code" 
```

### Logging

**As code**

```python
import sys

from loguru import logger

from hexplorer.config import 

STDERR_HANDLER = [
    {
        "sink": sys.stderr,
        "format": "<level>{level:<8}</level>| <cyan>{function}</cyan> | <level>{message}</level>",
        "level": "DEBUG",
    },
]

logger.configure(handlers=STDERR_HANDLER)
```

Disable logging

```python
from loguru import logger

# Disable logger just for a module
logger.disable("hexplorer.api.lol.match")
# Remove all loggers
logger.remove()
```

**Using envorionment variables**

```bash
export LOGURU_FORMAT="<level>{level:<8}</level>| <cyan>{function}</cyan> | <level>{message}</level>"
export LOGURU_LEVEL="DEBUG"
```

Disable logging

```bash
export LOGURU_AUTOINIT="False"
```

**Using .env file**

```
LOGURU_FORMAT="<level>{level:<8}</level>| <cyan>{function}</cyan> | <level>{message}</level>"
LOGURU_LEVEL="DEBUG"
```


## Special mentions

Again, I want to mention these two projects which helped generate more than half the code for this project:

- [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) 
- [riotapi-schema](https://github.com/MingweiSamuel/riotapi-schema)

Special thanks to the following projects from which I've drawn inspiration (In no specific order):

- [riot-watcher](https://github.com/pseudonym117/Riot-Watcher)
- [cassiopeia](https://github.com/meraki-analytics/cassiopeia)
- [pyot](https://github.com/paaksing/Pyot)