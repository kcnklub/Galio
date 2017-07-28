import time

from Galio import Galio
from Galio.Galio import GalioException
from Galio import parameters as params

key = input("Key: ")
w = Galio(api_key=key)


def wait():
    if not w.can_make_request():
        time.sleep(1)

# champion API test
try:
    print('Testing Champion API...')
    champion_id = input("Enter Champion id: ")
    champion = w.get_champion(champion_id=champion_id)
    all_champions = w.get_all_champions()
    FTP_champions = w.get_all_champions(free_to_play=True)
    wait()
    print("")
    print("Champion")
    print(champion)
    print("")
    print("All Champions")
    print(all_champions)
    print("")
    print("Free to play champions")
    print(FTP_champions)
except GalioException as e:
    print("Error: " + str(e))

me = None
try:
    print('Testing Summoner API...')
    summoner_name = input("SummonerName: ")
    me = w.get_summoner_by_summoner_name(summoner_name=summoner_name)
    me_by_id = w.get_summoner_by_id(me['id'])
    me_by_account_id = w.get_summoner_by_account_id(me['accountId'])
    wait()
    print(me)
    print(me_by_id)
    print(me_by_account_id)

except GalioException as e:
    print("Error: " + str(e))

try:
    print('Test Spectator Api')
    active_game = w.get_active_game_info_by_summoner_id(me['accountId'])

    print('Active Game: ')
    print(active_game)

    print('Featured games: ')
    print(w.get_featured_games())
    wait()

except GalioException as e:
    print("Error: " + str(e))

try:
    print('Test Match API')
    ranked_matches = w.get_ranked_matchlist(me['accountId'])
    print(ranked_matches['matches'][0])
    a_ranked_match = w.get_match_by_id(ranked_matches['matches'][0]['gameId'], for_account_id=me['accountId'])
    print(a_ranked_match)
    wait()
except GalioException as e:
    print('Error: ' + str(e))

try:
    print('Test Champion Mastery API')
    champ_mastery = w.get_champion_mastery_by_summoner_id(me['id'])
    print(champ_mastery)
    print(w.get_total_mastery_score(me['id']))
    wait()
except GalioException as e:
    print('Error: ' + str(e))

try:
    print('League API')
    challenger = w.get_challenger_league(queue=params.queue_ranked['solo'])
    master = w.get_master_league(queue=params.queue_ranked['solo'])
    summoner_league_information = w.get_league_by_summoner_id(me['id'])
    ladder_pos = w.get_ladder_position(me['id'])
    print('Solo Challenger Ladder')
    print(challenger)
    print('Solo master Ladder')
    print(master)
    print(me['name'] + " League Information")
    print(summoner_league_information)
    print(me['name'] + " Ladder Position")
    print(ladder_pos)
    wait()
except GalioException as e:
    print('Error: ' + str(e))

try:
    print('Static Data API')
    # print(w.get_static_champions())
    print(w.get_static_champions_by_id(245))
    # print(w.get_static_item())
    print(w.get_static_item_by_id(3029))
    print(w.get_static_masteries_by_id(6131))
    print(w.get_static_runes_by_id(5273))
    # print(w.get_static_profile_icon())
    print(w.get_static_summoner_spells())

    wait()
except GalioException as e:
    print('Error: ' + str(e))


try:
    print('Testing Masteries API...')
    my_masteries = w.get_masteries_by_summoner_id(me['id'])
    print(my_masteries)
    wait()
except GalioException as e:
    print('Error: ' + str(e))

try:
    print('Testing Runes API...')
    my_runes = w.get_rune_pages_by_summoner_id(me['id'])
    print(my_runes)
    wait()
except GalioException as e:
    print('Error: ' + str(e))

