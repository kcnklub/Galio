from lol_api import LolApi
from lol_api import parameters as params

w = LolApi('RGAPI-1b9dc6ef-143b-4386-b956-3b81168259bd')


# champion API test
def champion_api_test():
    ekko = w.get_champion(245)
    all_champions = w.get_all_champions()
    FTP_champions = w.get_all_champions(free_to_play=True)

    print("")
    print("ekko")
    print(ekko)
    print("")
    print("All Champions")
    print(all_champions)
    print("")
    print("Free to play champions")
    print(FTP_champions)


# summoner API Test
def summoner_api_test():
    me = w.get_summoner_by_summoner_name('kcnklub')
    me_by_id = w.get_summoner_by_id(me['id'])
    me_by_account_id = w.get_summoner_by_account_id(me['accountId'])

    print(me)
    print(me_by_id)
    print(me_by_account_id)


summoner_api_test()