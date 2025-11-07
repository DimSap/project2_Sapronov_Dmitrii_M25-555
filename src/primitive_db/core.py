
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
            # Skip ID field if provided by user - it's added automatically
            continue
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


def _is_value_of_type(value, expected_type):
    if expected_type == "int":
        return isinstance(value, int)
    if expected_type == "str":
        return isinstance(value, str)
    if expected_type == "bool":
        return isinstance(value, bool)
    return False


def _matches(record, where_clause):
    for key, expected in where_clause.items():
        if record.get(key) != expected:
            return False
    return True


def insert(metadata, table_name, values, table_data=None):
    if table_name not in metadata:
        print(f"Ошибка: Таблица \"{table_name}\" не существует.")
        return table_data if table_data is not None else []

    schema = metadata[table_name]
    ordered_columns = [column for column in schema.keys() if column != RESERVED_ID_NAME]

    if len(values) != len(ordered_columns):
        print("Некорректное количество значений. Попробуйте снова.")
        return table_data if table_data is not None else []

    if table_data is None:
        table_data = []

    for column_name, value in zip(ordered_columns, values):
        expected_type = schema[column_name]
        if not _is_value_of_type(value, expected_type):
            print(f"Некорректный тип для столбца {column_name}. Ожидался {expected_type}.")
            return table_data

    if table_data:
        max_id = max(item.get(RESERVED_ID_NAME, 0) for item in table_data)
        new_id = max_id + 1
    else:
        new_id = 1

    new_record = {RESERVED_ID_NAME: new_id}
    for column_name, value in zip(ordered_columns, values):
        new_record[column_name] = value

    table_data.append(new_record)
    print(f"Запись с ID={new_id} успешно добавлена в таблицу \"{table_name}\".")
    return table_data


def select(table_data, where_clause=None):
    if not where_clause:
        return table_data

    return [record for record in table_data if _matches(record, where_clause)]


def update(table_data, set_clause, where_clause, table_name=None):
    changed_ids = []
    for record in table_data:
        if _matches(record, where_clause):
            for key, value in set_clause.items():
                record[key] = value
            changed_ids.append(record.get(RESERVED_ID_NAME))

    if not changed_ids:
        print("Записи по условию не найдены.")
        return table_data

    if len(changed_ids) == 1:
        if table_name:
            print(f"Запись с ID={changed_ids[0]} в таблице \"{table_name}\" успешно обновлена.")
        else:
            print(f"Запись с ID={changed_ids[0]} успешно обновлена.")
    else:
        joined = ", ".join(str(item) for item in changed_ids)
        if table_name:
            print(f"Записи с ID={joined} в таблице \"{table_name}\" успешно обновлены.")
        else:
            print(f"Записи с ID={joined} успешно обновлены.")
    return table_data


def delete(table_data, where_clause, table_name=None):
    remaining = []
    deleted_ids = []
    for record in table_data:
        if _matches(record, where_clause):
            deleted_ids.append(record.get(RESERVED_ID_NAME))
        else:
            remaining.append(record)

    if not deleted_ids:
        print("Записи по условию не найдены.")
        return table_data

    if len(deleted_ids) == 1:
        if table_name:
            print(f"Запись с ID={deleted_ids[0]} успешно удалена из таблицы \"{table_name}\".")
        else:
            print(f"Запись с ID={deleted_ids[0]} успешно удалена из таблицы.")
    else:
        joined = ", ".join(str(item) for item in deleted_ids)
        if table_name:
            print(f"Записи с ID={joined} успешно удалены из таблицы \"{table_name}\".")
        else:
            print(f"Записи с ID={joined} успешно удалены из таблицы.")
    return remaining


