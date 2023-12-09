from .models import Summoner, Match, Champion
from .utils import UrlHandler, DataDragon


class LeagueAPI:

    def __init__(self, api_key="", platform="kr", region="asia"):   
        self.api_handler = UrlHandler(api_key=api_key)
        self.platform = platform
        self.region = region

    def get_summoner_by_riotId(self, gameName, tagLine):
        """Get a summoner by riot id (gameName + tagLine)

            Return -> puuid
        """
        url = f'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'
        return self._get_summoner(url)

    def get_summoner_by_name(self, summoner_name):
        """Get a summoner by summoner name
        """
        url = f'https://{self.platform}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
        return self._get_summoner(url)

    def get_summoner_by_puuid(self, puuid):
        """Get a summoner by PUUID
        """
        url = f'https://{self.platform}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'
        return self._get_summoner(url)

    def get_summoner_by_summonerId(self, id):
        """Get a summoner by summoner ID
        """
        url = f'https://{self.platform}.api.riotgames.com/lol/summoner/v4/summoners/{id}'
        return self._get_summoner(url)

    def get_summoner_by_accountId(self, accountId):
        """Get a summoner by account ID
        """
        url = f'https://{self.platform}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{accountId}'
        return self._get_summoner(url)

    def _get_summoner(self, url):
        res = self.api_handler.request(url=url)

        return Summoner(
                    self.api_handler,
                    platform=self.platform, 
                    region=self.region,
                    **res
                )

    def get_match(self, matchId):
        """Get a match by match id
        """
        return self._get_match(matchId=matchId)

    def _get_match(self, matchId):
        url = f'https://{self.region}.api.riotgames.com/lol/match/v5/matches/{matchId}'
        res = self.api_handler.request(url=url)

        return Match(**res)

    def get_champion_rotations(self):
        """Returns free champion ids and free champion ids for new players
            - Maximum new player level is res["maxNewPlayerLevel"].
        """
        url = f'https://{self.platform}.api.riotgames.com/lol/platform/v3/champion-rotations'
        res = self.api_handler.request(url=url)

        return res


def get_champion_by_id(championId, dd:DataDragon):
    champion = {}
    data = dd.all_champion_data()
    for _, v in data.items():  
        champion[v["key"]] = v
    try:
        return Champion(**champion[str(championId)])
    except KeyError:
        raise KeyError("It's not valid championId")
            

def get_champion_by_name(championName, dd:DataDragon):
    """
    Example => Lux(O), lux(X), LUX(X)
    """
    data = dd.all_champion_data()
    try:
        return Champion(**data[championName])
    except KeyError:
        raise KeyError("It's not valid championName")
