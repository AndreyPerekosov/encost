import psycopg2
import pandas as pd
import sys
import xlrd

# settings db
DB_SETTINGS = "host=localhost port=5432 dbname=vba user=user password=123"


# Create connect to DB
# conn = psycopg2.connect(DB_SETTINGS)

# open cursor
# cur = conn.cursor()

# execute cursor
# cur.execute("CREATE TABLE endpoint ("
#             "endpoint_id serial PRIMARY KEY,"
#             "endpoint_name varchar);")

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


def main():
    file_path = sys.argv[1]
    excel_data_df = pd.read_excel(file_path, sheet_name='Лист1')
    data = (excel_data_df.to_dict(orient='records'))
    cu_items(data=data)


if __name__ == '__main__':
    main()
