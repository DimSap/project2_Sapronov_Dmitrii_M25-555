import os
import shlex

import prompt

from src.primitive_db.core import create_table, drop_table
from src.primitive_db.utils import load_metadata, save_metadata

META_FILEPATH = os.path.join(os.path.dirname(__file__), "db_meta.json")


def print_help():
    """Prints the help message for the current mode."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def _save_if_changed(before, after):
    if before != after:
        save_metadata(META_FILEPATH, after)


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

        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Некорректное значение: {e}. Попробуйте снова.")
            continue

        command = args[0]
        if command == 'help':
            print_help()
            continue
        if command == 'exit':
            break

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

