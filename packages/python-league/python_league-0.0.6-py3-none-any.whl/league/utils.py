import requests


class DataDragon:
    """
    Currently, the latest version is 13.12.1

    - To get different language result, set different language parameter.

    **It is not always updated immediately after a patch according to Riot Games.**
    """
    def __init__(self, version="13.21.1", language="ko_KR") -> None:
        self.base_url = "https://ddragon.leagueoflegends.com/"
        self.version = self._check_version(version)
        self.language = language

    def all_champion_data(self):
        data = requests.get(f"{self.base_url}cdn/{self.version}/data/{self.language}/champion.json").json()
    
        return data['data']

    def _check_version(self, version):
        versions = requests.get(self.base_url+"api/versions.json")
        
        versions = versions.json()
        if version in versions:
            return version
        else:
            raise ValueError("It's not valid version")


class UrlHandler:
    def __init__(self, api_key) -> None:
        self._api_key = api_key
        self._request_headers = {
            "X-Riot-Token": self.api_key
        }
    
    @property
    def api_key(self):
        """
        Get: api_key
        """
        return self._api_key
 
    def request(self, url, params=None):
        res = requests.get(
            url=url,
            headers=self._request_headers,
            params=params
        )
        res.raise_for_status()

        return res.json()
