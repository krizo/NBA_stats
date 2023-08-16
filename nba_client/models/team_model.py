from dataclasses import dataclass


@dataclass
class TeamModel:
    id: int
    abbreviation: str
    name: str
    nickname: str
    city: str
    state: str
    year_founded: int
