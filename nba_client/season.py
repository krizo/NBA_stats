from datetime import datetime


class Season:
    def __init__(self, start_year: int = None):
        if not start_year:
            if datetime.today().month >= 9:
                start_year = datetime.today().year
            else:
                start_year = datetime.today().year - 1
        self.start_year = start_year
        self.end_year = start_year + 1

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return f"{self.start_year}-{str(self.end_year)[2:]}"
