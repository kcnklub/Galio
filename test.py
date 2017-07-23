from lol_api import LolApi
from lol_api import parameters as params

w = LolApi('RGAPI-c56ab87a-ceaa-4fe1-b88d-7fbb5ca325de')

me = w.get_summoner_by_summoner_name('kcnklub')
cool_guy = w.get_match_by_id(2549266921, for_account_id=me['accountId'])
cool_guy2 = w.get_match_by_id(2549266921)

print(cool_guy2['participantIdentities'])
print(cool_guy['participantIdentities'])


print(params.tags.all)