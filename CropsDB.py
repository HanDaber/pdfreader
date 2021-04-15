import sqlite3

db_name = 'TEST_DB_1'
table_name = 'crops_table_1'

labels = ['row_id', 'job_id',        'crop_image_name',  'left', 'top',  'width', 'height']
types = ['INTEGER', 'TEXT NOT NULL', 'TEXT',             'TEXT', 'TEXT', 'TEXT',  'TEXT']
value_placeholders = '?,?,?,?,?,?'

def _table():
    return table_name

def init():
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()
        wat_l = list(zip(labels[1:], types[1:]))
        # Return string zip of n
        def thinger(n):
            return f'{n[0]} {n[1]}'
        l = list(map(thinger, wat_l))
        columns = ', '.join(l)
        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

def find(job_id):
    rows = []
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()
        cols = ['rowid', 'job_id', 'crop_image_name', 'left', 'top', 'width', 'height']
        for row in cur.execute(f'SELECT {", ".join(cols)} FROM {table_name} WHERE job_id = \'{job_id}\''):
            it = iter(row)
            res_dct = dict(zip(cols, it))
            rows.append(res_dct)
    return rows

def insert(row_data):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        row = [row_data]
        cur.executemany(f'INSERT INTO {table_name} VALUES ({value_placeholders})', row)
        con.commit()

def insert_rows(rows):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()
        cur.executemany(f'INSERT OR IGNORE INTO {table_name} VALUES ({value_placeholders})', rows)
        con.commit()