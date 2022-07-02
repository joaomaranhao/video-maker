import json
from entities.match_data import MatchData


def save(data: MatchData) -> None:
    with open('./assets/match_data.json', 'w') as data_file:
        json.dump(data, data_file)


def load() -> MatchData:
    with open('./assets/match_data.json', 'r') as data_file:
        match_data = json.load(data_file)
    return match_data
