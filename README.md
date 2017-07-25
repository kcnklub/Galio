# lol-api.py
Lol-api is a light wrapper for the Riot Games, League of Legends API. I built this for a learn project and for a future project that I plan on working on. I used Darquiche's project as inspiration for this. Check out his project [here](https://github.com/Darquiche/Riot-Observer).

## Installation
```
pip install lol-api
```
## API Versions
| Name | Version |
--- | --- 
Champion | V3
Summoner | V3
Spectator | V3
Match | V3
Champion Mastery | V3
League | V3
Static Data | V3 
Masteries | V3
Runes | V3
## Examples
```
from LolApi import LolApi
from LolApi import LolException

x = LolApi('your-api-key')
```
### Summoner API
You can get summoner information by name, id, and AccountId
```
summoner = x.get_summoner_by_name('summoner-id')
```
### Champion API