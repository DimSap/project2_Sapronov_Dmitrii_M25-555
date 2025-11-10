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

- Через Poetry (скрипт `database`):
```bash
poetry run database
```

- Или через Makefile:
```bash
make run
```

Команды схемы
-------------
- **create_table**: `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...` — создать таблицу. Автоматически добавляется столбец `ID:int`.
- **list_tables**: `list_tables` — показать список всех таблиц.
- **drop_table**: `drop_table <имя_таблицы>` — удалить таблицу.
- **help** / **exit** — справка и завершение работы.

CRUD-операции
-------------
- **insert**: `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — добавить запись (столбец `ID` заполняется автоматически).
- **select**: `select from <имя_таблицы>` или `select from <имя_таблицы> where <столбец> = <значение>` — вывести записи с фильтрацией.
- **update**: `update <имя_таблицы> set <столбец> = <значение> where <столбец_условия> = <значение>` — изменить найденные строки.
- **delete**: `delete from <имя_таблицы> where <столбец> = <значение>` — удалить найденные строки.
- **info**: `info <имя_таблицы>` — отобразить схему и количество записей.

Подсказки
---------
- Поддерживаемые типы: `int`, `str`, `bool`.
- Строковые значения записывайте в двойных кавычках, булевы — `true`/`false`.
- Все данные сохраняются между запусками в JSON файлах.

Работа декораторов
-----------------
- Централизованная обработка ошибок через декоратор `handle_db_errors`: понятные сообщения при `FileNotFoundError`, `KeyError` и `ValueError`.
- Подтверждение опасных операций (`drop_table`, `delete`) с помощью `confirm_action` — выполнение продолжается только после ответа `y`.
- Замер времени для операций работы с файлами (`insert`, `select`) через `log_time`.
- Кэширование повторяющихся запросов выбора записей: одинаковые `select` выполняются быстрее за счет замыкания с внутренним кэшем.

Хранение данных
---------------
Метаданные находятся в `src/primitive_db/db_meta.json`. Каждая таблица хранит записи в отдельном файле `src/primitive_db/data/<имя_таблицы>.json`.

Пример использования
--------------------
```
***База данных***

***Операции с данными***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись
<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию
<command> select from <имя_таблицы> - прочитать все записи
<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение> - обновить записи
<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить записи
<command> info <имя_таблицы> - вывести информацию о таблице
Строковые значения указывайте в двойных кавычках.

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
>>>Введите команду: insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".

>>>Введите команду: select from users where age = 28
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei | 28  |    True   |
+----+--------+-----+-----------+

>>>Введите команду: update users set age = 29 where name = "Sergei"
Запись с ID=1 в таблице "users" успешно обновлена.

>>>Введите команду: delete from users where ID = 1
Запись с ID=1 успешно удалена из таблицы "users".

>>>Введите команду: info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0
```

Запуск
------
```
make project
```

Демонстрация
------------
Демонстрация запуска БД, создание, проверку и удаление таблицы

[![asciicast](https://asciinema.org/a/cjb2UNtT8qwanVE30cWiy5MmO.svg)](https://asciinema.org/a/cjb2UNtT8qwanVE30cWiy5MmO)



Демонстрация всех CRUD-операций.

[![asciicast](https://asciinema.org/a/a8Bn3Ob7BGpbYkZexVBiF4JJI.svg)](https://asciinema.org/a/a8Bn3Ob7BGpbYkZexVBiF4JJI)

Демонстрация работы Декораторов.

[![asciicast](https://asciinema.org/a/5h38fx0GSQ5A0SmX91pHidRPR.svg)](https://asciinema.org/a/5h38fx0GSQ5A0SmX91pHidRPR)