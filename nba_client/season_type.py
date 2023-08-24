class SeasonType:
    SEASON_TYPES = {
        '001': 'Pre Season',
        '002': 'Regular',
        '003': 'All-Star',
        '004': 'Post Season'
    }

    def __init__(self, season_id: str):
        self.name = self.SEASON_TYPES.get(season_id, 'Unknown')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
