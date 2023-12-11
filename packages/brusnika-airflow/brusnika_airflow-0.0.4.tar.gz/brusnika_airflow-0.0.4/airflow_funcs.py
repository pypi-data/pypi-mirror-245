"""
Частоиспользуемые функции в различных дагах.
"""

import pendulum
import sqlalchemy


def grants_for_table(pg_hook, schema, table):
    """Выдача прав"""
    pg_hook.run(
        f"GRANT INSERT, TRIGGER, REFERENCES, SELECT, UPDATE, DELETE, TRUNCATE\
          ON TABLE {schema}.{table} TO superset_lake;"
    )


def generate_table_name_for_temp_store(table_prefix):
    """Генерация имени для временной таблицы"""
    now = pendulum.now()
    date = now.to_date_string().replace("-", "")

    # Тире в названии таблицы ломает sql-запрос
    return f"{table_prefix}_{date}_{now.int_timestamp}"


def create_empty_table_like_this(
    pg_hook,
    source_schema,
    source_table,
    destination_schema,
    destination_table,
):
    """Создание пустой таблицы с аналогичной структурой
    Нужно чтобы наполнить эту таблицу с помощью PostgresHook.insert_rows"""

    query = f"CREATE TABLE {destination_schema}.{destination_table}\
              AS TABLE {source_schema}.{source_table} WITH NO DATA;"

    pg_hook.run(query)


def copy_data_between_tables(
    pg_hook,
    source_schema,
    source_table,
    destination_schema,
    destination_table,
):
    """Очистка таблицы, копирование в нее данных из промежуточной таблицы,
    удаление промежуточной таблицы"""

    if table_exists(pg_hook, destination_schema, destination_table):
        query = f"BEGIN;\
                  TRUNCATE TABLE {destination_schema}.{destination_table};\
                  INSERT INTO {destination_schema}.{destination_table} SELECT * FROM {source_schema}.{source_table};\
                  DROP TABLE {source_schema}.{source_table};\
                  COMMIT;"
    else:
        query = f"BEGIN;\
                  CREATE TABLE {destination_schema}.{destination_table} AS TABLE {source_schema}.{source_table};\
                  DROP TABLE {source_schema}.{source_table};\
                  COMMIT;"

    pg_hook.run(query)


def copy_data_between_tables_without_trancate(
    pg_hook,
    source_schema,
    source_table,
    destination_schema,
    destination_table,
):
    """Копирование в таблицу данных из промежуточной таблицы, удаление промежуточной таблицы"""

    if table_exists(pg_hook, destination_schema, destination_table):
        query = f"BEGIN;\
                  INSERT INTO {destination_schema}.{destination_table} SELECT * FROM {source_schema}.{source_table};\
                  DROP TABLE {source_schema}.{source_table};\
                  COMMIT;"
    else:
        query = f"BEGIN;\
                  CREATE TABLE {destination_schema}.{destination_table} AS TABLE {source_schema}.{source_table};\
                  DROP TABLE {source_schema}.{source_table};\
                  COMMIT;"

    pg_hook.run(query)


def copy_data_between_tables_with_deleting_data(
    pg_hook,
    source_schema,
    source_table,
    destination_schema,
    destination_table,
    delete_clause,
):
    """Копирование в таблицу данных из промежуточной таблицы,
    удаление данных из промежуточной таблицы"""

    if table_exists(pg_hook, destination_schema, destination_table):
        query = f"BEGIN;\
                  DELETE FROM {destination_schema}.{destination_table} WHERE {delete_clause};\
                  INSERT INTO {destination_schema}.{destination_table} SELECT * FROM {source_schema}.{source_table};\
                  DROP TABLE {source_schema}.{source_table};\
                  COMMIT;"
    else:
        query = f"BEGIN;\
                  CREATE TABLE {destination_schema}.{destination_table} AS TABLE {source_schema}.{source_table};\
                  DROP TABLE {source_schema}.{source_table};\
                  COMMIT;"

    pg_hook.run(query)


def table_exists(pg_hook, schema, table):
    """Есть такая таблица или нет в PG?"""

    query = f"SELECT EXISTS (SELECT * FROM information_schema.tables WHERE \
              table_schema LIKE '{schema}' AND table_name = '{table}')"

    result = pg_hook.get_first(sql=query)
    return result[0]


def dtypes_for_sql(dataframe, json_columns):
    """Формируем dtype для использования в df.to_sql"""

    dtypes = {}

    for key, value_object in dataframe.dtypes.items():
        if key in json_columns:
            dtypes[key] = sqlalchemy.types.JSON
        else:
            value = str(value_object).lower()

            if value == "int64":
                dtypes[key] = sqlalchemy.types.Integer
            elif value == "float64":
                dtypes[key] = sqlalchemy.types.Float
            elif value == "str":
                dtypes[key] = sqlalchemy.types.Text
            elif value == "bool":
                dtypes[key] = sqlalchemy.types.Boolean
            elif value == "datetime64[ns]":
                dtypes[key] = sqlalchemy.types.Date
            else:
                dtypes[key] = sqlalchemy.types.Text

    return dtypes
