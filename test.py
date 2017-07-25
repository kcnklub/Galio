import time

from lol_api import LolApi
from lol_api.LoLApi import LolException
from lol_api import parameters as params

w = LolApi('RGAPI-5ec4f241-6e2c-4805-a91a-1ef5820c5819')

def wait():
    while not w.can_make_request():
        time.sleep(1)

# champion API test

try:
    print('Testing Champion API...')
    champion_id = input("Enter Champion id: ")
    champion = w.get_champion(champion_id=champion_id)
    all_champions = w.get_all_champions()
    FTP_champions = w.get_all_champions(free_to_play=True)

    print("")
    print("Champion")
    print(champion)
    print("")
    print("All Champions")
    print(all_champions)
    print("")
    print("Free to play champions")
    print(FTP_champions)
except LolException as e:
    print("Error: " + str(e))

me = None
try:
    print('Testing Summoner API...')
    summoner_name = input("SummonerName: ")
    me = w.get_summoner_by_summoner_name(summoner_name=summoner_name)
    me_by_id = w.get_summoner_by_id(me['id'])
    me_by_account_id = w.get_summoner_by_account_id(me['accountId'])


    print(me)
    print(me_by_id)
    print(me_by_account_id)

except LolException as e:
    print("Error: " + str(e))

try:
    print('Test Spectator Api')
    active_game = w.get_active_game_info_by_summoner_id(me['accountId'])

    print('Active Game: ')
    print(active_game)

    print('Featured games: ')
    print(w.get_featured_games())

except LolException as e:
    print("Error: " + str(e))

try:
    print('Test Match API')
    ranked_matches = w.get_ranked_matchlist(me['accountId'])
    print(ranked_matches['matches'][0])
    a_ranked_match = w.get_match_by_id(ranked_matches['matches'][0]['gameId'], for_account_id=me['accountId'])
    print(a_ranked_match)

except LolException as e:
    print('Error: ' + str(e))

try:
    print('Test Champion Mastery API')
    champ_mastery = w.get_champion_mastery_by_summoner_id(me['accountId'])

    print(champ_mastery)
    print(w.get_total_mastery_score(me['accountId']))

except LolException as e:
    print('Error: ' + str(e))


