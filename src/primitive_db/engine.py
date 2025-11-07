import os
import shlex

import prompt
from prettytable import PrettyTable

from src.primitive_db.core import create_table, delete, drop_table, insert, select, update
from src.primitive_db.parser import parse_set_clause, parse_values_list, parse_where_clause
from src.primitive_db.utils import load_metadata, load_table_data, save_metadata, save_table_data

META_FILEPATH = os.path.join(os.path.dirname(__file__), "db_meta.json")


def print_help():
    """Prints the help message for the current mode."""
    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию")
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение> - обновить записи")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить записи")
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    print("Строковые значения указывайте в двойных кавычках.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def _save_if_changed(before, after):
    if before != after:
        save_metadata(META_FILEPATH, after)


def _value_matches_type(value, expected_type):
    if expected_type == "int":
        return isinstance(value, int)
    if expected_type == "str":
        return isinstance(value, str)
    if expected_type == "bool":
        return isinstance(value, bool)
    return False


def _validate_values(schema, values):
    ordered_columns = [column for column in schema.keys() if column != "ID"]
    for column_name, value in zip(ordered_columns, values):
        expected_type = schema[column_name]
        if not _value_matches_type(value, expected_type):
            print(f"Некорректный тип для столбца {column_name}. Ожидался {expected_type}.")
            return False
    return True


def _validate_clause(schema, clause):
    for key, value in clause.items():
        if key not in schema:
            print(f"Некорректное значение: {key}. Попробуйте снова.")
            return False
        expected_type = schema[key]
        if not _value_matches_type(value, expected_type):
            print(f"Некорректный тип для столбца {key}. Ожидался {expected_type}.")
            return False
    return True


def _print_table(schema, rows):
    headers = list(schema.keys())
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row([row.get(column, "") for column in headers])
    print(table)


def _handle_insert(metadata, raw_command):
    lower_command = raw_command.lower()
    keyword = " values"
    values_index = lower_command.find(keyword)
    if values_index == -1:
        print("Некорректное значение: values. Попробуйте снова.")
        return

    head = raw_command[:values_index].strip()
    if not head.lower().startswith("insert into "):
        print("Некорректное значение: insert. Попробуйте снова.")
        return

    head_parts = head.split()
    if len(head_parts) < 3:
        print("Некорректное значение: имя_таблицы. Попробуйте снова.")
        return

    table_name = head_parts[2]
    if table_name not in metadata:
        print(f"Ошибка: Таблица \"{table_name}\" не существует.")
        return

    schema = metadata[table_name]
    values_part = raw_command[values_index + len(keyword):].strip()
    if not values_part.startswith("(") or not values_part.endswith(")"):
        print("Некорректное значение: скобки. Попробуйте снова.")
        return

    raw_values = values_part[1:-1]
    parsed_values = parse_values_list(raw_values)

    if not _validate_values(schema, parsed_values):
        return

    table_data = load_table_data(table_name)
    before_count = len(table_data)
    updated_data = insert(metadata, table_name, parsed_values, table_data)
    if len(updated_data) > before_count:
        save_table_data(table_name, updated_data)


def _handle_select(metadata, raw_command):
    lower_command = raw_command.lower()
    keyword = "select from "
    rest = raw_command[len(keyword):] if lower_command.startswith(keyword) else ""
    if not rest:
        print("Некорректное значение: имя_таблицы. Попробуйте снова.")
        return

    lower_rest = rest.lower()
    where_keyword = " where "
    where_index = lower_rest.find(where_keyword)
    if where_index == -1:
        table_name = rest.strip()
        where_clause = None
    else:
        table_name = rest[:where_index].strip()
        where_raw = rest[where_index + len(where_keyword):].strip()
        where_clause = parse_where_clause(where_raw)
        if not where_clause:
            print("Некорректное значение: условие. Попробуйте снова.")
            return

    if table_name not in metadata:
        print(f"Ошибка: Таблица \"{table_name}\" не существует.")
        return

    schema = metadata[table_name]
    if where_clause and not _validate_clause(schema, where_clause):
        return

    table_data = load_table_data(table_name)
    rows = select(table_data, where_clause)
    if not rows:
        print("Записи по условию не найдены.")
        return

    _print_table(schema, rows)


def _handle_update(metadata, raw_command):
    lower_command = raw_command.lower()
    if not lower_command.startswith("update "):
        print("Некорректное значение: update. Попробуйте снова.")
        return

    content = raw_command[len("update "):]
    lower_content = lower_command[len("update "):]

    set_keyword = " set "
    where_keyword = " where "
    set_index = lower_content.find(set_keyword)
    if set_index == -1:
        print("Некорректное значение: set. Попробуйте снова.")
        return

    table_name = content[:set_index].strip()
    after_set = content[set_index + len(set_keyword):]
    lower_after_set = lower_content[set_index + len(set_keyword):]

    where_index = lower_after_set.find(where_keyword)
    if where_index == -1:
        print("Некорректное значение: where. Попробуйте снова.")
        return

    set_raw = after_set[:where_index].strip()
    where_raw = after_set[where_index + len(where_keyword):].strip()

    if table_name not in metadata:
        print(f"Ошибка: Таблица \"{table_name}\" не существует.")
        return

    schema = metadata[table_name]
    set_clause = parse_set_clause(set_raw)
    if "ID" in set_clause:
        print("Изменение столбца ID запрещено.")
        return

    if not _validate_clause(schema, set_clause):
        return

    where_clause = parse_where_clause(where_raw)
    if not where_clause:
        print("Некорректное значение: условие. Попробуйте снова.")
        return

    if not _validate_clause(schema, where_clause):
        return

    table_data = load_table_data(table_name)
    before_snapshot = [dict(record) for record in table_data]
    updated_data = update(table_data, set_clause, where_clause, table_name)
    if before_snapshot != updated_data:
        save_table_data(table_name, updated_data)


def _handle_delete(metadata, raw_command):
    lower_command = raw_command.lower()
    if not lower_command.startswith("delete from "):
        print("Некорректное значение: delete. Попробуйте снова.")
        return

    rest = raw_command[len("delete from "):]
    lower_rest = lower_command[len("delete from "):]
    where_keyword = " where "
    where_index = lower_rest.find(where_keyword)
    if where_index == -1:
        print("Некорректное значение: where. Попробуйте снова.")
        return

    table_name = rest[:where_index].strip()
    where_raw = rest[where_index + len(where_keyword):].strip()

    if table_name not in metadata:
        print(f"Ошибка: Таблица \"{table_name}\" не существует.")
        return

    schema = metadata[table_name]
    where_clause = parse_where_clause(where_raw)
    if not where_clause:
        print("Некорректное значение: условие. Попробуйте снова.")
        return

    if not _validate_clause(schema, where_clause):
        return

    table_data = load_table_data(table_name)
    before_count = len(table_data)
    updated_data = delete(table_data, where_clause, table_name)
    if len(updated_data) != before_count:
        save_table_data(table_name, updated_data)


def _handle_info(metadata, raw_command):
    parts = raw_command.split()
    if len(parts) != 2:
        print("Некорректное значение: имя_таблицы. Попробуйте снова.")
        return

    table_name = parts[1]
    if table_name not in metadata:
        print(f"Ошибка: Таблица \"{table_name}\" не существует.")
        return

    schema = metadata[table_name]
    table_data = load_table_data(table_name)
    columns_desc = ", ".join(f"{name}:{value}" for name, value in schema.items())
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns_desc}")
    print(f"Количество записей: {len(table_data)}")


def run():
    """Main REPL loop for table management."""
    print("***База данных***")
    print_help()

    while True:
        metadata = load_metadata(META_FILEPATH)
        try:
            user_input = prompt.string('>>>Введите команду: ')
        except (EOFError, KeyboardInterrupt):
            print()
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        lower_input = user_input.lower()

        if lower_input == 'help':
            print_help()
            continue
        if lower_input == 'exit':
            break

        if lower_input.startswith('insert into '):
            _handle_insert(metadata, user_input)
            continue

        if lower_input.startswith('select from '):
            _handle_select(metadata, user_input)
            continue

        if lower_input.startswith('update '):
            _handle_update(metadata, user_input)
            continue

        if lower_input.startswith('delete from '):
            _handle_delete(metadata, user_input)
            continue

        if lower_input.startswith('info '):
            _handle_info(metadata, user_input)
            continue

        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Некорректное значение: {e}. Попробуйте снова.")
            continue

        command = args[0]
        if command == 'list_tables':
            for name in metadata.keys():
                print(f"- {name}")
            continue

        if command == 'create_table':
            if len(args) < 3:
                missing = 'параметры' if len(args) == 1 else 'столбцы'
                print(f"Некорректное значение: {missing}. Попробуйте снова.")
                continue
            table_name = args[1]
            columns = args[2:]
            before = metadata
            after = create_table(before, table_name, columns)
            _save_if_changed(before, after)
            continue

        if command == 'drop_table':
            if len(args) != 2:
                bad = args[2:] if len(args) > 2 else 'имя_таблицы'
                print(f"Некорректное значение: {bad}. Попробуйте снова.")
                continue
            table_name = args[1]
            before = metadata
            after = drop_table(before, table_name)
            _save_if_changed(before, after)
            continue

        print(f"Функции {command} нет. Попробуйте снова.")

