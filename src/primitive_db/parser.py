import shlex


def parser_insert(command, metadata):
    args = shlex.split(command.replace("(", "").replace(")", "").replace(",", " "))
    table_name = args[2]
    values = args[4:]
    return metadata, table_name, values

def parse_value(value):
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Некорректное значение: {value}")

def parser_select(command):
    args = shlex.split(command, posix=False)
    table_name = args[2]
    where_clause = {}
    if len(args) > 3:
        column = args[4]
        value = parse_value(args[6])
        where_clause[column] = value
    else:
        where_clause = None

    return table_name, where_clause

def parser_update(command):
    args = shlex.split(command, posix=False)
    table_name = args[1]
    set_clause = {args[3]: parse_value(args[5])}
    where_clause = {args[7]: parse_value(args[9])}
    return table_name, set_clause, where_clause

def parser_delete(command):
    args = shlex.split(command, posix=False)
    table_name = args[2]
    where_clause = {args[4]: parse_value(args[6])}
    return table_name, where_clause

