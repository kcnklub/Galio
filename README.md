# Galio
Galio is a light wrapper for the Riot Games, League of Legends API. I built this for a learning project and for a future
 project that I plan on working on. I used Darquiche's project as inspiration for this. 
 Check out his project [here](https://github.com/Darquiche/Riot-Observer).

## Installation
```
pip install Galio
```
## Parameters
Along with Galio there is a params file that can be used to access tag 
strings and queue strings instead of manually typing them out. For 
example for the ranked solo queue string. 
```python
>>>from Galio import parameters as params
>>>param.queue_ranked['solo']
RANKED_SOLO_5x5
```
Also with queue strings there are all of the string for regions and tags used in the static data API
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
from Galio import Galio
from Galio import GalioException

x = Galio('your-api-key')
```
### Tip
I found that Riots API switch between using the summoner id, 'id' in the summoner object, and the account id. I did my best to define which one to use with which functions. 
### Summoner API
You can get summoner information by name, id, and AccountId
```python
summoner = x.get_summoner_by_name('summoner-id')
```
### Champion API
The champion API allows you to call for all champions or get a certain champion by id or free to play champions.
```python
all_champions = x.get_all_champions()
FTP_champions = x.get_all_champions(free_to_play='true')
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
```python
match = x.get_match_by_id(match-id)
ranked_match_history = x.get_ranked_matchlist(account-id)
recent_match_history = x.get_recent_matchlist(account-id)
match_timeline = x.get_match_timeline(match-id)
```
### Champion Mastery API
Information about champion mastery based on account and champion.
```python
champion_mastery_list = x.get_champion_mastery_by_summoner_id(summoner-id)
champion_mastery_champion = x.get_champion_mastery_by_summoner_id_and_champion_id(summoner-id, champion-id)
total_mastery = x.get_total_mastery_score(summoner-id)
```
### League API
Get ranked information
```python
challenger = x.get_challenger_league()
master = x.get_master_league()
summoner_league_information = x.get_league_by_summoner_id(summoner-id)
ladder_pos = x.get_ladder_position(summoner-id)
```
### Static Information
Get static data about the game. Every call in the Riot's API is included since there is so many I am not going to write all of them.
 Take a look in source for the rest they are all documented and should
 be easy to understand. 
```python
x.get_static_champions()
x.get_static_champions_by_id(245)
x.w.get_static_item()
x.get_static_item_by_id(3029)
x.get_static_masteries_by_id(6131)
x.get_static_runes_by_id(5273)
x.get_static_profile_icon()
x.get_static_summoner_spells()
```
### Masteries
Get the mastery information of a summoner
```python
masteries = x.get_masteries_by_summoner_id(summoner-id)
```
### Runes
Get the rune information of a summoner
```python
runes = x.get_rune_pages_by_summoner_id(summoner-id)
```

### Contributing
Feel free to if you find a bug with this code to start an issue on the github page it will be much appreciated. 

### Disclaimer
Galio isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc. 