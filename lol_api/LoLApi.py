"""
some information that i dont have.
"""
from urllib.request import urlopen, Request
import json
from lol_api import parameters as params

__title__ = 'LolApi'
__author__ = 'Kyle Miller'
__license__ = 'MIT'
__version__ = '0.0.1'


class LolApi:

    def __init__(self, api_key, region=params.NORTH_AMERICA):
        self.api_key = api_key
        self.region = region

    def _base_request(self, url, region, static=False, **kwargs):
        if region is None:
            region = self.region
        args = {'X-Riot-Token': self.api_key}
        opt_params = '?'
        for arg in kwargs:
            if kwargs[arg] is not None:
                opt_params = opt_params + str(arg) + "=" + str(kwargs[arg]) + "&"
        request_string = 'https://{region}.api.riotgames.com/lol/{static}{url}'.format(
            region=region,
            static='static-data/' if static else '',
            url=url,
            apiKey=self.api_key
        )
        req = Request(request_string + opt_params, headers=args)
        r = urlopen(req)
        return json.loads(r.read().decode('utf-8'))

    # champion API
    def _champion_request(self, end_url, region, **kwargs):
        return self._base_request(
            'platform/v{version}/champions{end_url}'.format(
                version=params.api_version['champion'],
                end_url=end_url
            ),
            region,
            **kwargs
        )

    # done
    def get_champion(self, champion_id, region=None):
        return self._champion_request(
            '/{id}'.format(
                id=champion_id
            ), 
            region
        )

    # done
    def get_all_champions(self, region=None, free_to_play=False):
        return self._champion_request(
            '?freeToPlay={free_to_play}'.format(
                free_to_play='true' if free_to_play else 'false'
            ), 
            region
        )

    # summoner API
    def _summoner_request(self, end_url, region=None, **kwargs):
        return self._base_request(
            'summoner/v{summoner_version}/summoners/{end_url}'.format(
                summoner_version=params.api_version['summoner'],
                end_url=end_url
            ),
            region, 
            **kwargs
        )

    # done
    def get_summoner_by_summoner_id(self, summoner_id, region=None):
        return self._summoner_request(
            '{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # done
    def get_summoner_by_account_id(self, account_id, region=None):
        return self._summoner_request(
            'by-account/{account_id}'.format(
                account_id=account_id
            ),
            region
        )

    # done
    def get_summoner_by_summoner_name(self, summoner_name, region=None):
        return self._summoner_request(
            'by-name/{summoner_name}'.format(
                summoner_name=summoner_name
            ),
            region
        )

    # spectator API
    def _spectator_request(self, end_url, region=None, **kwargs):
        return self._base_request(
            'spectator/v{spectator_version}/{end_url}'.format(
                spectator_version = params.api_version['spectator'],
                end_url=end_url
            ),
            region,
            **kwargs
        )

    # done
    def get_active_game_info_by_summoner_id(self, summoner_id, region=None):
        return self._spectator_request(
            'active-games/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # done
    def get_featured_games(self, region=None):
        return self._spectator_request(
            'featured-games',
            region
        )

    # match API
    def _match_request(self, end_url, region=None, **kwargs):
        return self._base_request(
            'match/v{match_version}/{end_url}'.format(
                end_url=end_url,
                match_version=params.api_version['match']
            ),
            region, 
            **kwargs
        )

    # done
    def get_match_by_id(self, match_id, region=None, for_account_id=None):
        return self._match_request(
            'matches/{match_id}'.format(
                match_id=match_id
            ),
            region,
            forAccountId=for_account_id
        )

    # done
    def get_ranked_matchlist(self, account_id, region=None, queue=None, begin_time=None, end_index=None, season=None, champion=None, begin_index=None, end_time=None):
        
        return self._match_request(
            'matchlists/by-account/{account_id}'.format(
                account_id=account_id
            ),
            region,
            queue=queue,
            beginTime=begin_time,
            endIndex=end_index,
            season=season,
            champion=champion,
            beginIndex=begin_index,
            endTime=end_time
        )

    # done
    def get_recent_matchlist(self, account_id, region=None):
        return self._match_request(
            'matchlists/by-account/{account_id}/recent'.format(
                account_id=account_id
            ),
            region
        )

    # done
    def get_match_timeline(self, match_id, region=None):
        return self._match_request(
            'timelines/by-match/{match_id}'.format(
                match_id=match_id
            ),
            region
        )

    # Champion Mastery API
    def _champion_mastery_request(self, end_url, region=None, **kwargs):
        return self._base_request(
            'champion-mastery/v{champion_mastery_version}/{end_url}'.format(
                end_url=end_url,
                champion_mastery_version=params.api_version['champion_mastery']
            ),
            region,
            **kwargs
        )

    # done
    def get_champion_mastery_by_summoner_id(self, summoner_id, region=None):
        return self._champion_mastery_request(
            'champion-masteries/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region,
        )

    # done
    def get_champion_master_by_summoner_and_champion_id(self, summoner_id, champion_id, region=None):
        return self._champion_mastery_request(
            'champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}'.format(
                summoner_id=summoner_id,
                champion_id=summoner_id
            ),
            region
        )

    # done
    def get_total_mastery_score(self, summoner_id, region=None, ):
        return self._champion_mastery_request(
            'scores/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # League API
    def _league_request(self, end_url, region=None, **kwargs):
        return self._base_request(
            'league/v{league_version}/{end_url}'.format(
                end_url=end_url,
                league_version=params.api_version['league_version']
            ),
            region, 
            **kwargs
        )

    # done
    def get_challenger_league(self, queue, region=None):
        return self._league_request(
            'challengerleagues/by-queue/{queue}'.format(
                queue=queue
            ),
            region
        )

    # done
    def get_leagues_by_summoner_id(self, summoner_id, region=None):
        return self._league_request(
            'leagues/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # done
    def get_master_league(self, queue, region=None):
        return self._league_request(
            'masterleagues/by-queue/{queue}'.format(
                queue=queue
            ),
            region
        )

    # done
    def get_ladder_position(self, summoner_id, region=None):
        return self._league_request(
            'positions/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # Static Data api
    def _static_data_request(self, end_url, region=None, **kwargs):
        return self._base_request(
            'v{static_data_version}'.format(
                static_data_version=params.api_version['lol_static_data']
            ),
            region,
            static=True,
            **kwargs
        )

    def get_static_champions(self, region=None, locale=None, patch_version=None, tags=None, data_by_id=False):
        return self._static_data_request(
            'champions',
            region,
            locale=locale,
            version=patch_version,
            tags=tags,
            dataById=data_by_id
        )

    def get_static_champions_by_id(self, champion_id, region=None, locale=None, patch_version=None, tags=None):
        return self._static_data_request(
            'champions/{champion_id}'.format(
                champion_id=champion_id
            ),
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )
