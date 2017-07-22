from lol_api import LolApi
from lol_api import parameters as params

w = LolApi('RGAPI-c56ab87a-ceaa-4fe1-b88d-7fbb5ca325de')

print(w.get_featured_games())


