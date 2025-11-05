
ALLOWED_TYPES = {"int", "str", "bool"}
RESERVED_ID_NAME = "ID"


def _parse_columns(columns):
    """Parse and validate column specs of form name:type.

    Returns (ok, parsed_columns, error_value)
    parsed_columns is a list of (name, type) if ok is True, else empty list.
    error_value describes the incorrect value for messaging.
    """
    parsed = []
    seen_names = set()
    for raw in columns:
        if ":" not in raw:
            return False, [], raw
        name, type_str = raw.split(":", 1)
        name = name.strip()
        type_str = type_str.strip()
        if not name:
            return False, [], raw
        if name.upper() == RESERVED_ID_NAME:
            return False, [], name
        if type_str not in ALLOWED_TYPES:
            return False, [], type_str
        if name in seen_names:
            return False, [], name
        seen_names.add(name)
        parsed.append((name, type_str))
    return True, parsed, ""


def create_table(metadata, table_name, columns):
    """Create a table definition inside metadata.

    - Adds ID:int automatically as the first column
    - Validates duplicates and allowed types
    - Prints user-facing messages
    Returns new metadata dict (may be the same if an error occurred).
    """
    if not table_name:
        print(f"Некорректное значение: {table_name}. Попробуйте снова.")
        return metadata

    if table_name in metadata:
        print(f"Ошибка: Таблица \"{table_name}\" уже существует.")
        return metadata

    ok, parsed_columns, err_val = _parse_columns(columns)
    if not ok:
        print(f"Некорректное значение: {err_val}. Попробуйте снова.")
        return metadata

    # Build ordered mapping: ID first
    new_table = {RESERVED_ID_NAME: "int"}
    for col_name, col_type in parsed_columns:
        new_table[col_name] = col_type

    new_metadata = dict(metadata)
    new_metadata[table_name] = new_table

    columns_desc = ", ".join([f"{RESERVED_ID_NAME}:int"] + [f"{n}:{t}" for n, t in parsed_columns])
    print(f"Таблица \"{table_name}\" успешно создана со столбцами: {columns_desc}")

    return new_metadata


def drop_table(metadata, table_name):
    """Drop a table definition from metadata if it exists. Prints messages."""
    if table_name not in metadata:
        print(f"Ошибка: Таблица \"{table_name}\" не существует.")
        return metadata

    new_metadata = dict(metadata)
    del new_metadata[table_name]
    print(f"Таблица \"{table_name}\" успешно удалена.")
    return new_metadata


