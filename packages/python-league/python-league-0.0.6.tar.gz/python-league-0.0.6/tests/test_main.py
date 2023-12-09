from league.models import *


class TestLeagueAPI:
    def test_get_summoner(self, api, summoner):
        assert api.get_summoner_by_name(summoner_name="Hide on bush")
        assert api.get_summoner_by_puuid(puuid="aWaw5qgWvUHiXJobplWwRyThWSfD45QhNF0Kgwt4JbZ-85bKAtjK6GJDzHzBCfJi_xn4rWqlTLSrdQ")
        assert api.get_summoner_by_accountId(accountId="nV1iqunmeDfpJCqwY-XVgRdVuCKdwBEnZpm3_R4xglz4")
        assert api.get_summoner_by_summonerId(id="X6szI2WCUz_fu1_bQa0tmnF7Oj2cGHaZfwkS0fGTbrfrhw")

        return isinstance(summoner, Summoner)

    def test_get_match(self, api):
        match = api.get_match(matchId="matchId")
        return isinstance(match, Match)

    def test_get_champion_by_id(self, api):
        return isinstance(api.get_champion_by_id(championId="championId"), Champion)

    def test_get_champion_by_name(self, api):
        return isinstance(api.get_champion_by_name(championName="championName"), Champion)