import psycopg2
import os
from psycopg2.sql import Identifier, SQL
import csv

# settings db
DB_SETTINGS = "host=localhost port=5433 dbname=sqlview user=user password=123"
NAME_MODELs_FOLDER = 'models'


def with_connect_db(settings):
    def decorator(func):
        def wrapper(*args, **kwargs):
            conn = psycopg2.connect(settings)
            cur = conn.cursor()
            func(cur, *args, **kwargs)
            conn.commit()
            cur.close()
            conn.close()

        return wrapper

    return decorator


@with_connect_db(DB_SETTINGS)
def cu_items(*args, **kwargs):
    c = args[0]
    data = kwargs['data']
    for item in data:
        c.execute("SELECT * FROM endpoint WHERE endpoint_id=(%s)", (item['endpoint_id'],))
        res = c.fetchone()
        if res:
            c.execute("UPDATE endpoint SET endpoint_name=(%s) WHERE endpoint_id=(%s)",
                      (item['endpoint_name'], item['endpoint_id']))
        else:
            c.execute("INSERT INTO endpoint (endpoint_name) VALUES (%s)", (item['endpoint_name'],))


@with_connect_db(DB_SETTINGS)
def create_tables(*args, **kwargs):
    c = args[0]
    tables_data = kwargs['data']
    for table_name, tables_path in tables_data.items():
        c.execute(SQL("CREATE TABLE {} (id serial PRIMARY KEY);").format(Identifier(table_name)))
        gen_row = read_csv(tables_path)
        table_cols = next(gen_row)
        for col in table_cols:
            c.execute(SQL("ALTER TABLE {} ADD COLUMN {} VARCHAR;").format(Identifier(table_name), Identifier(col)))
        count_id = 1
        for row in gen_row:
            first_entry = True
            for name_col, value in zip(table_cols, row):
                if first_entry:
                    c.execute(
                        SQL("INSERT INTO {} ({}) VALUES (%s)").format(Identifier(table_name), Identifier(name_col)),
                        (value,))
                    first_entry = False
                else:
                    c.execute(
                        SQL("UPDATE {} SET {}=(%s) WHERE id=(%s)").format(Identifier(table_name), Identifier(name_col)),
                        (value, count_id))
            count_id += 1

@with_connect_db(DB_SETTINGS)
def create_view_for_id(*args, **kwargs):
    c = args[0]
    tables_data = kwargs['view']
    el_id = kwargs['id']
    c.execute(SQL("CREATE VIEW {} AS"
                  "SELECT p.endpoint_id, p.mode_start,"
                  "to_char(p.mode_start::timestamp + (p.mode_duration || ' minute')::interval, 'YYYY-MM-DD HH24:MI:SS' || '+03') as mode_end,"
                  "p.mode_duration, p.label, r.reason, o.operator_name,"
                  "(SELECT SUM(e.kwh::float) FROM energy e WHERE event_time::timestamp BETWEEN "
                  "p.mode_start::timestamp "
                  "AND (p.mode_start::timestamp + (p.mode_duration || ' minute')::interval) "
                  "AND e.endpoint_id=p.endpoint_id) as energy_sum FROM periods as p"
                  "LEFT JOIN reasons as r on r.endpoint_id=p.endpoint_id "
                  "AND r.event_time::timestamp BETWEEN p.mode_start::timestamp "
                  "AND p.mode_start::timestamp + (p.mode_duration || ' minute')::interval"
                  "LEFT JOIN operators o on p.endpoint_id = o.endpoint_id "
                  "AND (o.login_time::timestamp BETWEEN p.mode_start::timestamp "
                  "AND (p.mode_start::timestamp + (p.mode_duration || ' minute')::interval) "
                  "OR (p.mode_start::timestamp BETWEEN o.login_time::timestamp "
                  "AND o.logout_time::timestamp)) WHERE p.endpoint_id::int=(%s)").format(Identifier(tables_data)), (el_id,))


# helper for read csv file
def read_csv(path):
    with open(path, newline='\n') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            yield row


def main():
    ## preparing data
    # cur_path = os.getcwd()
    # model_path = os.path.join(cur_path, NAME_MODELs_FOLDER)
    # models_paths = [os.path.join(model_path, item) for item in os.listdir(model_path)]
    # models_names = [item.split('.')[0] for item in os.listdir(model_path)]
    # data = {models_names[i]: models_pahts[i] for i in range(len(model_path))}
    # data = dict(zip(models_names, models_paths))
    ## create tables
    # create_tables(data=data)
    ## create view



if __name__ == '__main__':
    main()
