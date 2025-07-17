
CLEAR_TABLE = {ord('\xa0'): ' '}


def clear(raw: str) -> str:
    return raw.translate(CLEAR_TABLE)
