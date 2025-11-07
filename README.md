Управление таблицами
====================

Модуль предоставляет простейшую работу с таблицами и хранит метаданные в JSON (`db_meta.json`).

Установка
-------

- С Poetry:
```bash
poetry install
```

- Или через Makefile:
```bash
make install
```

Запуск
-------

- Через Poetry (скрипт `project`):
```bash
poetry run project
```

- Или через Makefile:
```bash
make project
```

Команды
-------
- **create_table**: `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...` — создать таблицу. Автоматически добавляется столбец `ID:int`.
- **list_tables**: `list_tables` — показать список всех таблиц.
- **drop_table**: `drop_table <имя_таблицы>` — удалить таблицу.
- **help**: `help` — показать справку.
- **exit**: `exit` — выйти.

Поддерживаемые типы данных: `int`, `str`, `bool`.

Пример использования
--------------------
```
***База данных***

***Процесс работы с таблицей***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу

Общие команды:
<command> exit - выход из программы
<command> help - справочная информация

>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>>Введите команду: create_table users name:str
Ошибка: Таблица "users" уже существует.

>>>Введите команду: list_tables
- users

>>>Введите команду: drop_table users
Таблица "users" успешно удалена.

>>>Введите команду: drop_table products
Ошибка: Таблица "products" не существует.

>>>Введите команду: help
***Процесс работы с таблицей***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу

Общие команды:
<command> exit - выход из программы
<command> help - справочная информация
```

Запуск
------
```
make database
```

Пример запуска 


[![asciicast](https://asciinema.org/a/cjb2UNtT8qwanVE30cWiy5MmO.svg)](https://asciinema.org/a/cjb2UNtT8qwanVE30cWiy5MmO)
