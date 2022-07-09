from dataclasses import dataclass


@dataclass
class Player:
    champion: str
    kda: str
    name: str
    rank: str


@dataclass
class Team:
    players: list[Player]
    result: str


@dataclass
class MatchData:
    duration: str
    loser: str
    mvp: Player
    patch: str
    region: str
    team1: Team
    team2: Team
    player_role: str
    player_index: str
