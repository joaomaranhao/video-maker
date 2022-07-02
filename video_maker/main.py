from usecases.data import load
from entities.match_data import MatchData
from entities.data_scrapper import DataScrapper
from usecases.scrap_lol_data import ScrapLolData
from usecases.create_thumbnail import CreateThumbnail

lol_data_scrapper = ScrapLolData()
lol_data_scrapper.get_match_data_and_download_replay()
lol_data: MatchData = load()
thumb_creator = CreateThumbnail(data_scrapper=DataScrapper(), data=lol_data)
thumb_creator.create_thumbnail()
