# python-league
Python-league는 Riot API를 사용하여 간편하게 리그 오브 레전드(롤) 데이터를 사용할 수 있도록 만든 python 라이브러리입니다.

# NOTICE
RiotGames is now recommending using Riot ID instead of summonerName. It supports getting information by summonerName right now, but it will be unsupported in the future.

<img src="img/example_riot_id.png" alt="example_riot_id" width=400>

## Installation
![Generic badge](https://img.shields.io/badge/pypi-v0.0.5-yellow.svg)
```
pip install python-league --upgrade
```

## Tutorial
Here's <a href="https://github.com/ah00ee/python-league/blob/main/tutorial.ipynb">tutorial</a> for your information.

## Region & Platform values
|Region|Platform|
|--|--|
|America|NA1|
||BR1|
||LA1|
||LA2|
|Asia|JP1|
||KR|
||PH2|
||SG2|
||TH2|
||TW2|
||VN2|
|Europe|EUN1|
||EUW1|
||TR1|
||RU|
|Sea|OC1|


## How to use
```python
from league import LeagueAPI

lol = LeagueAPI(api_key="Your API KEY")

summoner = lol.get_summoner_by_name(summoner_name="summoner name")
print(summoner.info())
```

## Warning
라이브러리 사용을 위해 Development API KEY를 발급받은 경우, Riot Games에서 rate limit을 1초에 20 requests, 2분에 100 requests로 제한하고 있습니다. 