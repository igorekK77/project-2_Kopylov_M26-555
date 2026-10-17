correct_type = ["int", "str", "bool"]

def create_table(metadata, table_name,
                 columns):
    if table_name in metadata:
        raise ValueError(f"Ошибка: Имя таблицы {table_name} "
                         f"уже использовано")

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

def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError(f"Ошибка: Таблицы {table_name} не существует")

    del metadata[table_name]
    return metadata