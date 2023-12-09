from league.models import Champion, ChampionMastery


class TestSummoner:
    def test_champion_mastery_list(self, summoner):
        top_champion = summoner.get_top_champion_mastery()
        all_champion = summoner.get_all_champion_mastery()
        assert isinstance(top_champion[0], ChampionMastery)
        assert isinstance(all_champion[0], ChampionMastery)

    def test_get_champion_mastery_by_championId(self, summoner):
        champion = summoner.get_champion_mastery_by_championId("5")
        assert isinstance(champion, ChampionMastery)


class TestChampion:
    def test_kwargs(self, api):
        champion_by_id = api.get_champion_by_id("5")
        assert isinstance(champion_by_name, Champion)
        champion_by_name = api.get_champion_by_name("Ahri")
        assert isinstance(champion_by_id, Champion)
        
        assert champion_by_id.__str__ == champion_by_id.id + " " + champion_by_id.key

