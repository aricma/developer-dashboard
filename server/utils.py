def limit_string(value: str, character_limit: int) -> str:
    length = len(value)
    if length <= character_limit:
        return value
    else:
        return value[0 : character_limit - 3] + "..."
