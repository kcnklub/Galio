"""
some information that i dont have.
"""
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
from lol_api import parameters as params
from collections import deque
import time

__title__ = 'LolApi'
__author__ = 'Kyle Miller'
__license__ = 'MIT'
__version__ = '0.0.1'


class LolException(Exception):
    def __init__(self, error, response):
        self.error = error
        self.headers = response.headers

    def __str__(self):
        return str(self.error)

    def __eq__(self, other):
        if isinstance(other, ''.__class__):
            return self.error == other
        elif isinstance(other, self.__class__):
            return self.error == other.error and self.headers == other.headers
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return super(LolException).__hash__()

error_400 = 'Bad request'
error_401 = 'Unauthorized'
error_403 = 'Blacklisted key'
error_404 = 'Game data not found'
error_405 = 'Method not allowed'
error_415 = 'Unsupported media type'
error_422 = "Player exists, but hasn't played since match history collection began"
error_429 = 'Too many requests'
error_500 = 'Internal server error'
error_502 = 'Bad gateway'
error_503 = 'Service unavailable'
error_504 = 'Gateway timeout'


def throw_lol_exception(response):
    if response.status == 400:
        raise LolException(error_400, response)
    elif response.status == 401:
        raise LolException(error_401, response)
    elif response.status == 403:
        raise LolException(error_403, response)
    elif response.status == 404:
        raise LolException(error_404, response)
    elif response.status == 405:
        raise LolException(error_405, response)
    elif response.status == 415:
        raise LolException(error_415, response)
    elif response.status == 422:
        raise LolException(error_422, response)
    elif response.status == 429:
        raise LolException(error_429, response)
    elif response.status == 500:
        raise LolException(error_500, response)
    elif response.status == 502:
        raise LolException(error_502, response)
    elif response.status == 503:
        raise LolException(error_503, response)
    elif response.status == 504:
        raise LolException(error_504, response)


class RateLimit:

    def __init__(self, allowed_calls, seconds):
        self.allowed_calls = allowed_calls
        self.seconds = seconds
        self.made_requests = deque()

    def __reload(self):
        t = time.time()
        while len(self.made_requests) > 0 and self.made_requests[0] < t:
            self.made_requests.popleft()

    def add_request(self):
        self.made_requests.append(time.time() + self.seconds)

    def request_available(self):
        self.__reload()
        return len(self.made_requests) < self.allowed_calls


class LolApi:

    def __init__(self, api_key, region=params.NORTH_AMERICA, limits=(RateLimit(10, 10), RateLimit(500, 600))):
        self.api_key = api_key
        self.region = region
        self.limits = limits

    def can_make_request(self):
        for lim in self.limits:
            if not lim.request_available():
                return False
        return True

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
        try:
            req = Request(request_string + opt_params, headers=args)
            r = urlopen(req)
        except HTTPError as e:
            throw_lol_exception(e)
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
            '',
            region,
            freeToPlay='true' if free_to_play else 'false'
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
    def get_summoner_by_id(self, summoner_id, region=None):
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
    def get_champion_mastery_by_summoner_and_champion_id(self, summoner_id, champion_id, region=None):
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

    def get_static_item(self, region=None, locale=None, patch_version=None, tags=None):
        return self._static_data_request(
            'items',
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_item_by_id(self, item_id, region=None, locale=None, patch_version=None, tags=None):
        return self._static_data_request(
            'items/{item_id}'.format(
                item_id=item_id
            ),
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_language_strings(self, region=None, locale=None, patch_version=None):
        return self._static_data_request(
            'language-strings',
            region,
            locale=locale,
            version=patch_version
        )

    def get_static_languages(self, region=None):
        return self._static_data_request(
            'languages',
            region,
        )

    def get_static_maps(self, region=None, locale=None, patch_version=None):
        return self._static_data_request(
            'maps',
            region,
            locale=locale,
            version=patch_version
        )

    def get_static_masteries(self, region=None, locale=None, patch_version=None, tags=None):
        return self._static_data_request(
            'masteries',
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_masteries_by_id(self, mastery_id, region=None, locale=None, patch_version=None, tags=None):
        return self._static_data_request(
            'masteries/{mastery_id}'.format(
                mastery_id=mastery_id
            ),
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_profile_icon(self, region=None, locale=None, patch_version=None):
        return self._static_data_request(
            'profile-icons',
            region,
            locale=locale,
            version=patch_version
        )

    def get_static_realms(self, region=None):
        return self._static_data_request(
            'realms',
            region
        )

    def get_static_runes(self, region=None, locale=None, patch_version=None, tags=None):
        return self._static_data_request(
            'runes',
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_runes_by_id(self, rune_id, region=None, locale=None, patch_version=None, tags=None):
        return self._static_data_request(
            'runes/{rune_id}'.format(
                rune_id=rune_id
            ),
            region,
            tags=tags,
            locale=locale,
            version=patch_version
        )

    def get_static_summoner_spells(self, region=None, locale=None, patch_version=None, tags=None, data_by_id=False):
        return self._static_data_request(
            'summoner-spells',
            region,
            locale=locale,
            version=patch_version,
            dataById=data_by_id,
            tags=tags
        )

    def get_static_summoner_spells_by_id(self, summoner_spell_id, region=None, locale=None, patch_version=None, tags=None):
        return self._static_data_request(
            'summoner-spells/{spell_id}'.format(
                spell_id=summoner_spell_id
            ),
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_versions(self, region=None):
        return self._static_data_request(
            'versions',
            region
        )

    # Masteries API
    def _masteries_request(self, end_url, region=None, **kwargs):
        return self._base_request(
            'platform/v{mastery_version}/{end_url}'.format(
                end_url=end_url,
                mastery_version=params.api_version['masteries']
            ),
            region,
            **kwargs
        )

    def get_masteries_by_summoner_id(self, summoner_id, region=None):
        return self._masteries_request(
            'masteries/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # Roons API
    def _runes_request(self, end_url, region=None, **kwargs):
        return self._base_request(
            'platform/v{runes_version}/{end_url}'.format(
                end_url=end_url,
                runes_version=params.api_version['runes']
            ),
            region,
            **kwargs
        )

    def get_rune_pages_by_summoner_id(self, summoner_id, region=None):
        return self._runes_request(
            'runes/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id,
            ),
            region
        )