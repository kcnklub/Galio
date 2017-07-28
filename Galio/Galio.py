from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
from Galio import parameters as params
from collections import deque
import time

__title__ = 'LolApi'
__author__ = 'Kyle Miller'
__license__ = 'MIT'
__version__ = '0.0.1'


class GalioException(Exception):
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
        return super(GalioException).__hash__()

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


def throw_galio_exception(response):
    if response.status == 400:
        raise GalioException(error_400, response)
    elif response.status == 401:
        raise GalioException(error_401, response)
    elif response.status == 403:
        raise GalioException(error_403, response)
    elif response.status == 404:
        raise GalioException(error_404, response)
    elif response.status == 405:
        raise GalioException(error_405, response)
    elif response.status == 415:
        raise GalioException(error_415, response)
    elif response.status == 422:
        raise GalioException(error_422, response)
    elif response.status == 429:
        raise GalioException(error_429, response)
    elif response.status == 500:
        raise GalioException(error_500, response)
    elif response.status == 502:
        raise GalioException(error_502, response)
    elif response.status == 503:
        raise GalioException(error_503, response)
    elif response.status == 504:
        raise GalioException(error_504, response)


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


class Galio:

    def __init__(self, api_key, region=params.NORTH_AMERICA, limits=(RateLimit(10, 10), RateLimit(500, 600))):
        self.api_key = api_key
        self.region = region
        self.limits = limits

    def can_make_request(self):
        """
        :return: Checks if you can make a request bases on rate limits.
        """
        for lim in self.limits:
            if not lim.request_available():
                return False
        return True

    def _base_request(self, url, region, static=False, **kwargs):
        """
        :param url: the end of the url for the request.
        :param region: default region override.
        :param static: True if trying to access static API.
        :param kwargs: Additional arguments
        :return:
        """
        if region is None:
            region = self.region
        args = {'X-Riot-Token': self.api_key}
        opt_params = '?'
        for arg in kwargs:
            if kwargs[arg] is not None:
                opt_params = opt_params + str(arg) + '=' + str(kwargs[arg]) + '&'
        opt_params = opt_params[:-1]
        request_string = 'https://{region}.api.riotgames.com/lol/{static}{url}'.format(
                region=region,
                static='static-data/' if static else '',
                url=url,
                )

        try:
            req = Request(request_string + opt_params, headers=args)
            print(request_string + opt_params)
            r = urlopen(req)
        except HTTPError as e:
            throw_galio_exception(e)
        else:
            if not static:
                for lim in self.limits:
                    lim.add_request()
            return json.loads(r.read().decode('utf-8'))

    # champion API
    def _champion_request(self, end_url, region, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
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
        """
        :param champion_id: id of champion searched.
        :param region: default region override
        :return: Json object of a single champion
        """
        return self._champion_request(
            '/{id}'.format(
                id=champion_id
            ), 
            region
        )

    # done
    def get_all_champions(self, region=None, free_to_play=False):
        """
        :param region: default region override
        :param free_to_play: filter to free to play champions
        :return: Json object of all champions(not Static Data)
        """
        return self._champion_request(
            '',
            region,
            freeToPlay='true' if free_to_play else 'false'
        )

    # summoner API
    def _summoner_request(self, end_url, region=None, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
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
        """
        :param summoner_id: summoner id of the summoner being searched.
        :param region: default region override
        :return: Json object of the summoner
        """
        return self._summoner_request(
            '{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # done
    def get_summoner_by_account_id(self, account_id, region=None):
        """
        :param account_id: account id of the summoner being searched.
        :param region: default region override
        :return: Json object of the summoner
        """
        return self._summoner_request(
            'by-account/{account_id}'.format(
                account_id=account_id
            ),
            region
        )

    # done
    def get_summoner_by_summoner_name(self, summoner_name, region=None):
        """
        :param summoner_name: String of summoner name
        :param region: default region override
        :return: Json object of the summoner
        """
        return self._summoner_request(
            'by-name/{summoner_name}'.format(
                summoner_name=summoner_name
            ),
            region
        )

    # spectator API
    def _spectator_request(self, end_url, region=None, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
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
        """
        :param summoner_id: summoner id of summoner being searched.
        :param region: default region override
        :return: a json object of active game if summoner is in a game.
        """
        return self._spectator_request(
            'active-games/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # done
    def get_featured_games(self, region=None):
        """
        :param region: default region override
        :return: Json object of featured game based on region
        """
        return self._spectator_request(
            'featured-games',
            region
        )

    # match API
    def _match_request(self, end_url, region=None, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
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
        """
        :param match_id: The id of the match
        :param region: default region override
        :param for_account_id: adds information about a participant of the match
        :return: Json object for a match
        """
        return self._match_request(
            'matches/{match_id}'.format(
                match_id=match_id
            ),
            region,
            forAccountId=for_account_id
        )

    # done
    def get_ranked_matchlist(self, account_id,
                             region=None,
                             queue=None,
                             begin_time=None,
                             end_index=None,
                             season=None,
                             champion=None,
                             begin_index=None,
                             end_time=None):
        """
        :param account_id: id of the account you are searching
        :param region: default region override
        :param queue: the type of queue
        :param begin_time: a beginning cut off.
        :param end_index:
        :param season: Which ranked season
        :param champion: filter by champion
        :param begin_index:
        :param end_time: ending cut off
        :return: Json MatchList
        """
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
        """
        :param account_id: Account id of summoner you are searching the matchlist of
        :param region: default region override.
        :return: Json object of the last 20 games ranked or unranked.
        """
        return self._match_request(
            'matchlists/by-account/{account_id}/recent'.format(
                account_id=account_id
            ),
            region
        )

    # done
    def get_match_timeline(self, match_id, region=None):
        """
        :param match_id: Id of the match that is being searched.
        :param region: default region override.
        :return: Json match object.
        """
        return self._match_request(
            'timelines/by-match/{match_id}'.format(
                match_id=match_id
            ),
            region
        )

    # Champion Mastery API
    def _champion_mastery_request(self, end_url, region=None, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
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
        """
        be sure to use summoner id not account id.
        :param summoner_id: Summoner id of summoner being searched.
        :param region: default region override.
        :return: Json object of champions and mastery score on those champions.
        """
        return self._champion_mastery_request(
            'champion-masteries/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region,
        )

    # done
    def get_champion_mastery_by_summoner_and_champion_id(self, summoner_id, champion_id, region=None):
        """
        be sure to use summoner id not account id.
        :param summoner_id: Summoner id of summoner being searched.
        :param champion_id: Champion you want to see the score of.
        :param region: default region override.
        :return: Json object of champion mastery for a specific summoner champion combo.
        """
        return self._champion_mastery_request(
            'champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}'.format(
                summoner_id=summoner_id,
                champion_id=champion_id
            ),
            region
        )

    # done
    def get_total_mastery_score(self, summoner_id, region=None, ):
        """
        :param summoner_id: summoner id of summoner being searched.
        :param region: default region override.
        :return: Total mastery score
        """
        return self._champion_mastery_request(
            'scores/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # League API
    def _league_request(self, end_url, region=None, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
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
        """
        :param queue: type of ranked queue that you are searching for.
        :param region: default region override.
        :return: Json object of challenger league.
        """
        return self._league_request(
            'challengerleagues/by-queue/{queue}'.format(
                queue=queue
            ),
            region
        )

    # done
    def get_league_by_summoner_id(self, summoner_id, region=None):
        """
        :param summoner_id: summoner id of summoner being searched.
        :param region: default region override.
        :return: Json object of ranked information for the summoner.
        """
        return self._league_request(
            'leagues/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # done
    def get_master_league(self, queue, region=None):
        """
        :param queue: type of ranked queue that you are searching for.
        :param region: default region override.
        :return: Json object of master league.
        """
        return self._league_request(
            'masterleagues/by-queue/{queue}'.format(
                queue=queue
            ),
            region
        )

    # done
    def get_ladder_position(self, summoner_id, region=None):
        """
        :param summoner_id: summoner id of summoner being searched.
        :param region: default region override.
        :return: Json object of a summoners ladder position
        """
        return self._league_request(
            'positions/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # Static Data api
    def _static_data_request(self, end_url, region=None, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
        return self._base_request(
            'v{static_data_version}/{end_url}'.format(
                end_url=end_url,
                static_data_version=params.api_version['lol_static_data']
            ),
            region,
            static=True,
            **kwargs
        )

    def get_static_champions(self, region=None, locale=None, patch_version=None, tags=None, data_by_id='false'):
        """
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :param data_by_id: if false will use champion keys not ids
        :return: Json object with static data on all champions.
        """
        return self._static_data_request(
            'champions',
            region,
            locale=locale,
            version=patch_version,
            tags=tags,
            dataById=data_by_id
        )

    def get_static_champions_by_id(self, champion_id, region=None, locale=None, patch_version=None, tags=None):
        """
        :param champion_id: champion id of champion being searched.
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :return: Json object with static data on the champion.
        """
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
        """
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :return: Json object with static data on all items.
        """
        return self._static_data_request(
            'items',
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_item_by_id(self, item_id, region=None, locale=None, patch_version=None, tags=None):
        """

        :param item_id: id of item being searched
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :return: Json object with static data on the item.
        """
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
        """
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :return: Json object of language strings
        """
        return self._static_data_request(
            'language-strings',
            region,
            locale=locale,
            version=patch_version
        )

    def get_static_languages(self, region=None):
        """
        :param region: default region override
        :return: Json object of languages.
        """
        return self._static_data_request(
            'languages',
            region,
        )

    def get_static_maps(self, region=None, locale=None, patch_version=None):
        """
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :return: Json object of
        """
        return self._static_data_request(
            'maps',
            region,
            locale=locale,
            version=patch_version
        )

    def get_static_masteries(self, region=None, locale=None, patch_version=None, tags=None):
        """
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :return: Json object of masteries static information
        """
        return self._static_data_request(
            'masteries',
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_masteries_by_id(self, mastery_id, region=None, locale=None, patch_version=None, tags=None):
        """
        :param mastery_id: mastery id of mastery being searched.
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :return: Json object of a single mastery
        """
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
        """
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :return: Json object of all profile icons.
        """
        return self._static_data_request(
            'profile-icons',
            region,
            locale=locale,
            version=patch_version
        )

    def get_static_realms(self, region=None):
        """
        :param region: default region override
        :return: Json object of static realms. """
        return self._static_data_request(
            'realms',
            region
        )

    def get_static_runes(self, region=None, locale=None, patch_version=None, tags=None):
        """
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :return: Json object of all runes
        """
        return self._static_data_request(
            'runes',
            region,
            locale=locale,
            version=patch_version,
            tags=tags
        )

    def get_static_runes_by_id(self, rune_id, region=None, locale=None, patch_version=None, tags=None):
        """
        :param rune_id: id of rune being searched.
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :return: Json object of the rune
        """
        return self._static_data_request(
            'runes/{rune_id}'.format(
                rune_id=rune_id
            ),
            region,
            tags=tags,
            locale=locale,
            version=patch_version
        )

    def get_static_summoner_spells(self, region=None, locale=None, patch_version=None, tags=None, data_by_id='false'):
        """
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :param data_by_id: if false will use champion keys not ids
        :return: Json object with information of all summoner spells.
        """
        return self._static_data_request(
            'summoner-spells',
            region,
            locale=locale,
            version=patch_version,
            dataById=data_by_id,
            tags=tags
        )

    def get_static_summoner_spells_by_id(self, summoner_spell_id,
                                         region=None,
                                         locale=None,
                                         patch_version=None,
                                         tags=None):
        """

        :param summoner_spell_id: Id of the summoner spell being searched.
        :param region: default region override.
        :param locale: locale of search. If None will use region
        :param patch_version: version of patch you are looking for default current.
        :param tags: Changes the output
        :return: Json object with information of the summoner spell
        """
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
        """
        :param region: default region override.
        :return: Json object of versions
        """
        return self._static_data_request(
            'versions',
            region
        )

    # Masteries API
    def _masteries_request(self, end_url, region=None, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
        return self._base_request(
            'platform/v{mastery_version}/{end_url}'.format(
                end_url=end_url,
                mastery_version=params.api_version['masteries']
            ),
            region,
            **kwargs
        )

    def get_masteries_by_summoner_id(self, summoner_id, region=None):
        """
        :param summoner_id: summoner id of summoner being searched.
        :param region: default region override
        :return: Json object of summoners mastery pages.
        """
        return self._masteries_request(
            'masteries/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id
            ),
            region
        )

    # Roons API
    def _runes_request(self, end_url, region=None, **kwargs):
        """
        :param end_url: end of the request string
        :param region: region override.
        :param kwargs: any add additional arguments.
        :return:
        """
        return self._base_request(
            'platform/v{runes_version}/{end_url}'.format(
                end_url=end_url,
                runes_version=params.api_version['runes']
            ),
            region,
            **kwargs
        )

    def get_rune_pages_by_summoner_id(self, summoner_id, region=None):
        """
        :param summoner_id: summoner id of summoner being searched.
        :param region: default region override
        :return: Json object of summoners runes pages.
        """
        return self._runes_request(
            'runes/by-summoner/{summoner_id}'.format(
                summoner_id=summoner_id,
            ),
            region
        )