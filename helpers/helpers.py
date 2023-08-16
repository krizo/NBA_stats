def find_in_collection(collection: list, attribute: str, expected_value: any) -> dict or None:
    try:
        return next(team for team in collection if team.get(attribute) == expected_value)
    except StopIteration:
        return None


def lists_to_dict(headers: list, data: list) -> dict:
    return dict(map(lambda i, j: (i, j), headers, data))


def convert_to_metric(feet: int, inches: int, precision: int = 0) -> int or float:
    return round((feet * 12 + inches) * 2.54, precision)


def assert_equals(actual: any, expected: any, description: str):
    """Asserts the two values are equal, or raises error including the provided description."""
    assert actual == expected, f"{description}, expected: '{expected}' != actual: '{actual}'"