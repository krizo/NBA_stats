def find_in_collection(collection: list, attribute: str, expected_value: any):
    try:
        return next(team for team in collection if team.get(attribute) == expected_value)
    except StopIteration:
        return None
