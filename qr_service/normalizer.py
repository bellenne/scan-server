def normalize_code(raw: str) -> str:
    """
    'AG-BR-010_400x270|0'        -> 'AG-BR-010_400x270'
    '123456|4|AG-BR-010_400x270' -> 'AG-BR-010_400x270'
    """
    raw = (raw or "").strip()
    parts = raw.split("|")

    if len(parts) <= 2:
        return parts[0]
    return parts[-1]
