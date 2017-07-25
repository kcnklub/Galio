﻿# lol-api.py
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
```python
from LolApi import LolApi
from LolApi import LolException

x = LolApi('your-api-key')
```
### Summoner API
You can get summoner information by name, id, and AccountId
```python
summoner = x.get_summoner_by_name('summoner-id')
```
### Champion API
The champion API allows you to call for all champions or get a certain champion by id or free to play champions.
```python
all_champions = x.get_all_champions()
FTP_champions = x.get_all_champions(free_to_play=True)
ekko = x.get_champion_by_id(245)
```
### Spectator API
This is used for getting Active games of players by id and Featured games. 
```python
active_match = x.get_active_game_info_by_summoner_id(summoner-id)
featured_games = x.get_featured_games()
```
### Match API
You are able to get recent match history, ranked match history, match details, and match timelines from this API
```
match = x.get_match_by_id(match-id)
ranked_match_history = x.get_ranked_matchlist(account-id)
recent_match_history = x.get_recent_matchlist(account-id)
match_timeline = x.get_match_timeline(match-id)
```
### Champion Mastery API
Information about champion mastery based on account and champion.
```
champion_mastery_list = x.get_champion_mastery_by_summoner_id(summoner-id)
champion_mastery_champion = x.get_champion_mastery_by_summoner_id_and_champion_id(summoner-id, champion-id)
total_mastery = x.get_total_mastery_score(summoner-id)
```
### League API
Get ranked information
```
challenger = x.get_challenger_league()
master = x.get_master_league()
summoner_league_information = x.get_league_by_summoner_id(summoner-id)
ladder_pos = x.get_ladder_position(summoner-id)
```
### Static Information
Get static data about the game. Every call in the Riot's API is included since there is so many I am not going to write them out here, and the use of ddragon isn't used. Take a look in source. 
### Masteries
Get the mastery information of a summoner
```
masteries = x.get_masteries_by_summoner_id(summoner-id)
```
### Runes
Get the rune information of a summoner
```
runes = x.get_rune_pages_by_summoner_id(summoner-id)
```
