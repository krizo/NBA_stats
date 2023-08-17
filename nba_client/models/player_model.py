from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class PlayerModel:
    id: int
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    birth_date: datetime
    school: str
    country: str
    height: int
    weight: int
    position: str
    current_number: int
    current_team_abbreviation: str
    current_team_id: int
    first_season_played: int
    draft_year: int
    draft_number: int

    @property
    def age(self) -> int:
        return int((datetime.now() - self.birth_date).days / 365.25)
