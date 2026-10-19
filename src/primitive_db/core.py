from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import load_table_data

correct_type = ["int", "str", "bool"]

@handle_db_errors
@log_time
def create_table(metadata, table_name,
                 columns):
    if table_name in metadata:
        raise ValueError(f"Имя таблицы {table_name} "
                         f"уже использовано")

    if "ID:int" not in columns:
        columns = ["ID:int"] + columns
    dict_columns = {}
    for column in columns:
        name, type_column = column.split(":")
        if type_column.lower() not in correct_type:
            raise TypeError(f"Тип {type_column} не "
                            f"поддерживается")
        dict_columns[name] = type_column
    metadata[table_name] = dict_columns
    return metadata

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError(f"Таблицы {table_name} не существует")

    del metadata[table_name]
    return metadata

@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        raise ValueError(f"Таблицы {table_name} не существует")
    if len(values) != len(metadata[table_name]) - 1:
        raise ValueError("Количество переданных значений "
                         "не соответствует количеству столбцов")
    type_columns = [type_column for column, type_column in metadata[table_name].items()
                    if column != "ID"]
    converted_values = []
    for value, column_type in zip(values, type_columns):
        if column_type == "int":
            try:
                converted_value = int(value)
            except (TypeError, ValueError):
                raise ValueError(f"Значение {value} не является типом int")

        elif column_type == "bool":
            if value not in ["true", "false"]:
                raise ValueError(f"Переданное значение {value} не является типом bool")
            converted_value = value == "true"
        else:
            converted_value = str(value)

        converted_values.append(converted_value)

    table_data = load_table_data(table_name)

    new_id = max([id_data["ID"] for id_data in table_data], default=0) + 1
    new_line = {"ID":new_id}
    metadata_keys = [key for key in metadata[table_name] if key != "ID"]
    for key, value in zip(metadata_keys, converted_values):
        new_line[key] = value

    table_data.append(new_line)
    return table_data, new_id

@log_time
def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    filter_table_data = []
    key, value = list(where_clause.keys())[0], list(where_clause.values())[0]

    for data in table_data:
        if key in data and data[key] == value:
            filter_table_data.append(data)

    return filter_table_data

def update(table_data, set_clause, where_clause):
    key_set, value_set = list(set_clause.keys())[0], list(set_clause.values())[0]
    key_where, value_where = list(where_clause.keys())[0], list(where_clause
                                                                .values())[0]

    for data in table_data:
        if key_where in data and data[key_where] == value_where:
            if key_set in data:
                data[key_set] = value_set

    return table_data

@confirm_action("удаление строки")
def delete(table_data, where_clause):
    key, value = list(where_clause.keys())[0], list(where_clause.values())[0]
    table_data = [data for data in table_data if key not in data or data[key] != value]

    return table_data

@handle_db_errors
def info(table_name, metadata, table_data):
    if table_name not in metadata:
        raise ValueError(f"Таблицы с именем {table_name} не существует")
    first_line = f"Таблица: {table_name}\n"
    second_line = f"Столбцы: {", ".join(f"{name}:{type_column}" for name, type_column 
                                        in metadata[table_name].items())}\n"

    third_line = f"Количество записей: {len(table_data)}"
    return first_line + second_line + third_line