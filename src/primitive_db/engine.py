import prompt
import shlex

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata



filepath = "db_meta.json"

def run():
    print_help()
    while True:
        metadata = load_metadata(filepath)
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        command = args[0]
        table_name = args[1] if len(args) > 1 else None

        match command:
            case "create_table":
                columns = [column for column in args[2:]]
                try:
                    metadata = create_table(metadata, table_name, columns)
                except (ValueError, TypeError) as e:
                    print(e.args[0])
                    continue
                save_metadata(filepath, metadata)
                print(f"Таблица \"{table_name}\" успешно создана"
                      f"  со столбцами: {", ".join(f"{keys}:{values}" 
                      for keys, values in metadata[table_name].items())}")
            case "drop_table":
                try:
                    metadata = drop_table(metadata, table_name)
                except ValueError as e:
                    print(e.args[0])
                    continue
                save_metadata(filepath, metadata)
                print(f"Таблица \"{table_name}\" успешно удалена")
            case "list_tables":
                for name in metadata.keys():
                    print(f"- {name}")
            case "help":
                print_help()
            case "exit":
                return
            case _:
                print("Данная команда не сущесвтует!")



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