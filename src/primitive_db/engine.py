import prompt

HELP_LINES = (
    "<command> exit - выйти из программы",
    "<command> help - справочная информация",
)


def _print_help() -> None:
    for line in HELP_LINES:
        print(line)


def welcome() -> None:

    print('Первая попытка запустить проект!')
    print('***')
    _print_help()

    while True:
        command = prompt.string('Введите команду: ').strip().lower()
        if command == 'help':
            _print_help()
            continue
        if command == 'exit':
            break
        continue


