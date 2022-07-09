from time import sleep
from selenium.webdriver.common.by import By
from entities.data_scrapper import DataScrapper
from entities.match_data import MatchData, Player
from usecases.data import save


class ScrapLolData(DataScrapper):
    def __init__(self) -> None:
        super().__init__()
        # URL
        self.__url = 'https://www.leagueofgraphs.com/replays/with-high-kda/grandmaster/sr-ranked'
        self.__champions_xpath_selector = '//*[contains(concat( " ", @class, " " ), concat( " ", "relative", " " ))]//img'
        self.__match_table_selector = '//*[contains(concat( " ", @class, " " ), concat( " ", "matchTable", " " ))]'
        self.__region_xpath = '//*[(@id = "mainContent")]//a'
        self.__watch_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "replay_watch_button", " " ))]'
        self.__download_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "replayDownloadButton", " " ))]'
        self.match_data: MatchData = {
            "team1": {
                "players": []
            },
            "team2": {
                "players": []
            }
        }

    def get_match_data_and_download_replay(self) -> None:
        self.driver.get(self.__url)
        table = self.driver.find_element(
            by=By.XPATH, value=self.__match_table_selector)
        text_list = table.text.split('\n')
        self.match_data['team1']['result'] = text_list[0].split(' ')[0]
        self.match_data['team2']['result'] = text_list[0].split(' ')[-1]
        duration = text_list[0].split(' ')[3][1:-1]
        self.match_data['duration'] = duration
        patch = text_list[-1].split(' ')[1][1:-1]
        self.match_data['patch'] = patch
        elements = self.driver.find_elements(
            by=By.XPATH, value=self.__champions_xpath_selector)
        elements[0].get_dom_attribute('title')
        champions = self.__get_champions_names(elements=elements)
        self.match_data['team1']['players'] = self.__create_team_one(
            text_list=text_list, champions=champions)
        self.match_data['team2']['players'] = self.__create_team_two(
            text_list=text_list, champions=champions)
        mvp_data = self.__get_mvp_data(self.match_data)
        self.match_data['mvp'] = self.match_data[mvp_data['team']
                                                 ]['players'][mvp_data['player_index']]
        self.match_data['loser'] = self.match_data[mvp_data['loser_team']
                                                   ]['players'][mvp_data['player_index']]['champion']
        self.match_data['player_role'] = mvp_data['player_role']
        self.match_data['player_index'] = str(
            int(mvp_data['player_index']) + 1)
        region_link = self.driver.find_element(
            by=By.XPATH, value=self.__region_xpath)
        link_array = region_link.get_property('href').split('/')
        self.match_data['region'] = link_array[4].upper()
        # Save Data
        save(self.match_data)
        self.__download_match()
        self.quit()

    def __get_champions_names(self, elements: list) -> list[str]:
        champions = []
        for i in range(0, 38):
            if elements[i].get_dom_attribute('title') is not None:
                champions.append(elements[i].get_dom_attribute('title'))
        return champions

    def __create_player(self, name: str, kda: str, rank: str, champion: str) -> Player:
        return {
            "name": name,
            "kda": kda,
            "rank": rank,
            "champion": champion
        }

    def __create_team_one(self, text_list: list, champions: list) -> list[Player]:
        team_one = []
        team_one.append(self.__create_player(
            name=text_list[1], kda=text_list[3], rank=text_list[2], champion=champions[0]))
        team_one.append(self.__create_player(
            name=text_list[9], kda=text_list[11], rank=text_list[10], champion=champions[2]))
        team_one.append(self.__create_player(
            name=text_list[17], kda=text_list[19], rank=text_list[18], champion=champions[4]))
        team_one.append(self.__create_player(
            name=text_list[25], kda=text_list[27], rank=text_list[26], champion=champions[6]))
        team_one.append(self.__create_player(
            name=text_list[33], kda=text_list[35], rank=text_list[34], champion=champions[8]))
        return team_one

    def __create_team_two(self, text_list: list, champions: list) -> list[Player]:
        team_two = []
        team_two.append(self.__create_player(
            name=text_list[7], kda=text_list[5], rank=text_list[8], champion=champions[1]))
        team_two.append(self.__create_player(
            name=text_list[15], kda=text_list[13], rank=text_list[16], champion=champions[3]))
        team_two.append(self.__create_player(
            name=text_list[23], kda=text_list[21], rank=text_list[24], champion=champions[5]))
        team_two.append(self.__create_player(
            name=text_list[31], kda=text_list[29], rank=text_list[32], champion=champions[7]))
        team_two.append(self.__create_player(
            name=text_list[39], kda=text_list[37], rank=text_list[40], champion=champions[9]))
        return team_two

    def __get_mvp_data(self, match_data):
        team = ''
        kdas = []
        if match_data['team1']['result'] == 'Victory':
            for player in match_data['team1']['players']:
                team = 'team1'
                loser_team = 'team2'
                kdas.append(int(player['kda'].split(' ')[0]))
        else:
            for player in match_data['team2']['players']:
                team = 'team2'
                loser_team = 'team1'
                kdas.append(int(player['kda'].split(' ')[0]))
        player_index = kdas.index(max(kdas))
        roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
        return {
            "team": team,
            "player_index": player_index,
            "loser_team": loser_team,
            "player_role": roles[player_index]
        }

    def __download_match(self):
        watch_button = self.driver.find_element(
            by=By.XPATH, value=self.__watch_xpath)
        download_button = self.driver.find_element(
            by=By.XPATH, value=self.__download_xpath)
        self.driver.execute_script("arguments[0].click();", watch_button)
        sleep(1)
        self.driver.execute_script("arguments[0].click();", download_button)
        sleep(2)
