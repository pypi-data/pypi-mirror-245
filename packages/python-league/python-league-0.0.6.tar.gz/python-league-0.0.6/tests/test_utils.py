import requests

class TestDataDragon:

    def test_url(self):
        data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/13.21.1/data/ko_KR/champion.json")
        data.raise_for_status()
        versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        versions.raise_for_status()

