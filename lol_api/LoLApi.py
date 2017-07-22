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
        for arg in kwargs:
            if kwargs[arg] is not None:
                args[arg] = kwargs[arg]
        request_string = 'https://{region}.api.riotgames.com/lol/{static}{url}'.format(
            region=region,
            static='static/data/' if static else '',
            url=url,
            apiKey=self.api_key
        )
        req = Request(request_string, headers=args)
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

    def get_champion(self, champion_id, region=None):
        return self._champion_request(
            '/{id}'.format(
                id=champion_id
            ), region
        )

    def get_all_champions(self, region=None, free_to_play=False):
        return self._champion_request(
            '?freeToPlay={free_to_play}'.format(
                free_to_play='true' if free_to_play else 'false'
            ), region
        )

    # summoner API
    def _summoner_request(self, end_url, region=None):
        return self._base_request(
            'summoner/v{summoner_version}/summoners/{end_url}'.format(
                summoner_version=params.api_version['summoner'],
                end_url=end_url
            ),
            region
        )

    def get_summoner_by_summoner_id(self, summoner_id, region=None):
        return self._summoner_request(
            '{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    def get_summoner_by_account_id(self, account_id, region=None):
        return self._summoner_request(
            'by-account/{account_id}'.format(
                account_id=account_id
            ),
            region
        )

    def get_summoner_by_summoner_name(self, summoner_name, region=None):
        return self._summoner_request(
            'by-name/{summoner_name}'.format(
                summoner_name=summoner_name
            ),
            region
        )

    # spectator API
    def _spectator_request(self, end_url, region=None):
        return self._base_request(
            'spectator/v{spectator_version}/{end_url}'.format(
                spectator_version = params.api_version['spectator'],
                end_url=end_url
            ),
            region
        )

    def get_active_game_info_by_summoner_id(self, summoner_id, region=None):
        return self._spectator_request(
            'active-games/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    def get_featured_games(self, region=None):
        return self._spectator_request(
            'featured-games',
            region
        )

    # match API
    def _match_request(self, end_url, region=None):
        return self._base_request(
            'match/v{match_version}/{end_url}'.format(
                end_url=end_url,
                match_version=params.api_version['match']
            ),
            region
        )

    def get_match_by_id(self, match_id, region=None):
        return self._match_request(
            'matches/{match_id}'.format(
                match_id=match_id
            ),
            region
        )

    def get_ranked_matchlist(self, account_id, region=None):
        return self._match_request(
            'matchlists/by-account/{account_id}'.format(
                account_id=account_id
            ),
            region
        )

    def get_recent_matchlist(self, account_id, region=None):
        return self._match_request(
            'matchlists/by-account/{account_id}/recent'.format(
                account_id=account_id
            ),
            region
        )

    def get_match_timeline(self, match_id, region=None):
        return self._match_request(
            'timelines/by-match/{match_id}'.format(
                match_id=match_id
            ),
            region
        )

    def get_matches_by_tournament_id(self, tournament_code, region=None):
        return self._match_request(
            'matches/by-tournament-code/{tournament_code}/ids'.format(
                tournament_code=tournament_code
            ),
            region
        )

    def get_match_by_tournament_id_and_match_id(self, tournament_code, match_id, region=None):
        return self._match_request(
            'matches/{match_id}/by-tournament-code/{tournament_id}'.format(
                match_id=match_id,
                tournament_id=tournament_code
            ),
            region
        )

