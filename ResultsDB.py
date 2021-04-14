import sqlite3

db_name = 'TEST_DB_1'
table_name = 'results_table_1'

labels = ['row_id', 'job_id',        'symbol_id',            'symbol',        'symbol_probability', 'symbol_bounding_box', 'slice_file', 'value', 'value_probability', 'value_bounding_box']
types = ['INTEGER', 'TEXT NOT NULL', 'TEXT NOT NULL',        'TEXT NOT NULL', 'REAL',               'TEXT',                'TEXT',       'REAL',  'REAL',              'TEXT']
value_placeholders = '?,?,?,?,?,?,?,?,?'

def _table():
    return table_name

def init():
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        # Create table
        wat_l = list(zip(labels[1:], types[1:]))
        # print(f'wat_l: {str(wat_l)}')
        
        # Return string zip of n
        def thinger(n):
            return f'{n[0]} {n[1]}'

        l = list(map(thinger, wat_l))
        # print(f'l: {l}')

        # columns = [(a, b) for ((a), (b)) in l]
        columns = ', '.join(l)
        # print(f'columns: {str(columns)}')

        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns}, PRIMARY KEY(job_id, slice_file, symbol, symbol_id))')

def insert_rows(rows):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()
        cur.executemany(f'INSERT OR IGNORE INTO {table_name} VALUES ({value_placeholders})', rows)
        con.commit()

def insert(row):
    insert_rows([row])

def add_value(row_id, value, val_prob, val_bb):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        # row = [row_data]
        cur.execute(f'UPDATE {table_name} SET value = \'{value}\', value_probability = \'{val_prob}\', value_bounding_box = \'{val_bb}\' WHERE rowid = \'{row_id}\'')
        con.commit()

def find(job_id):
    rows = []

    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        # print('FOUND ROWS')
        cols = ['rowid', 'symbol', 'symbol_probability', 'symbol_bounding_box', 'slice_file', 'value', 'value_probability', 'value_bounding_box']
        for row in cur.execute(f'SELECT {", ".join(cols)} FROM {table_name} WHERE job_id = \'{job_id}\''):
            # print(row)
            it = iter(row)
            res_dct = dict(zip(cols, it))
            rows.append(res_dct)

    return rows