import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    select,
    update,
)
from primitive_db.decorators import create_cacher
from primitive_db.parser import (
    parser_delete,
    parser_insert,
    parser_select,
    parser_update,
)
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

filepath = "db_meta.json"

def run():
    print_help()
    cash = create_cacher()

    while True:
        metadata = load_metadata(filepath)
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        command = args[0]

        match command:
            case "create_table":
                columns = [column for column in args[2:]]
                table_name = args[1] if len(args) > 1 else None
                metadata = create_table(metadata, table_name, columns)
                if metadata is None:
                    continue
                save_metadata(filepath, metadata)
                print(f"Таблица \"{table_name}\" успешно создана"
                      f"  со столбцами: {", ".join(f"{keys}:{values}" 
                      for keys, values in metadata[table_name].items())}")
            case "drop_table":
                table_name = args[1] if len(args) > 1 else None
                metadata = drop_table(metadata, table_name)
                if metadata is None:
                    continue
                save_metadata(filepath, metadata)
                cash = create_cacher()
                print(f"Таблица \"{table_name}\" успешно удалена")
            case "list_tables":
                for name in metadata.keys():
                    print(f"- {name}")
            case "insert":
                metadata, table_name, values = parser_insert(user_input, metadata)
                result = insert(metadata, table_name, values)
                if result is None:
                    continue
                table_data, new_id = result
                save_table_data(table_name, table_data)
                cash = create_cacher()
                print(f"Запись с ID={new_id} успешно добавлена в "
                      f"таблицу \"{table_name}\"")
            case "select":
                table_name, where_clause = parser_select(user_input)
                table_data = load_table_data(table_name)
                filter_table_data = cash(user_input, lambda: select(table_data,
                                                                    where_clause))
                table = PrettyTable()
                table.field_names = list(metadata[table_name].keys())
                for row in filter_table_data:
                    table.add_row([row[column] for column in table.field_names])
                print(table)
            case "update":
                table_name, set_clause, where_clause = parser_update(user_input)
                table_data = load_table_data(table_name)
                found_records = select(table_data, where_clause)

                if not found_records:
                    print("Запись не найдена.")
                    continue

                record_id = found_records[0]["ID"]

                table_data = update(table_data, set_clause, where_clause)
                save_table_data(table_name, table_data)
                cash = create_cacher()
                print(f"Запись с ID={record_id} в таблице \"{table_name}\" "
                      f"успешно обновлена.")
            case "delete":
                table_name, where_clause = parser_delete(user_input)
                table_data = load_table_data(table_name)

                found_records = select(table_data, where_clause)

                if not found_records:
                    print("Запись не найдена.")
                    continue

                record_id = found_records[0]["ID"]

                table_data = delete(table_data, where_clause)
                save_table_data(table_name, table_data)
                cash = create_cacher()
                print(f"Запись с ID={record_id} успешно удалена из "
                      f"таблицы \"{table_name}\"")
            case "info":
                table_name = args[1]
                table_data = load_table_data(table_name)
                print(info(args[1], metadata, table_data))
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
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - "
          "создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, "
          "...) - создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - "
          "прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where "
          "<столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - "
          "удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")