def _split_values(raw):
    items = []
    current = []
    in_quotes = False
    for char in raw:
        if char == '"':
            in_quotes = not in_quotes
            current.append(char)
            continue
        if char == ',' and not in_quotes:
            item = ''.join(current).strip()
            if item:
                items.append(item)
            current = []
            continue
        current.append(char)
    if current:
        items.append(''.join(current).strip())
    return items


def _parse_value(raw):
    value = raw.strip()
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        return value[1:-1]

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False

    try:
        return int(value)
    except ValueError:
        return value


def parse_values_list(raw):
    if not raw:
        return []
    parts = _split_values(raw)
    return [_parse_value(part) for part in parts]


def parse_where_clause(raw):
    clause = raw.strip()
    if "=" not in clause:
        return {}
    left, right = clause.split("=", 1)
    key = left.strip()
    value = _parse_value(right)
    return {key: value}


def parse_set_clause(raw):
    assignments = {}
    for part in _split_values(raw):
        if "=" not in part:
            continue
        left, right = part.split("=", 1)
        key = left.strip()
        assignments[key] = _parse_value(right)
    return assignments


