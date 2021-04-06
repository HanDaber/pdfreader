import sqlite3

# db_name = ...
labels = ['row_id', 'date', 'job_id',               'status', 'qty', 'price']
types = ['INTEGER', 'TEXT', 'TEXT NOT NULL UNIQUE', 'TEXT', 'REAL', 'REAL']
value_placeholders = '?,?,?,?,?'

def init(db_name, table_name):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        # Create table
        wat_l = list(zip(labels[1:], types[1:]))
        print(f'wat_l: {str(wat_l)}')
        
        # Return string zip of n
        def thinger(n):
            return f'{n[0]} {n[1]}'

        l = list(map(thinger, wat_l))
        print(f'l: {l}')

        # columns = [(a, b) for ((a), (b)) in l]
        columns = ', '.join(l)
        print(f'columns: {str(columns)}')

        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

def hydrate(db_name, table_name):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        purchases = [('2006-03-28', 'ABC_123', 'PENDING', 1000, 45.00),
                    ('2006-04-05', 'CDE_234', 'PENDING', 1000, 72.00),
                    ('2006-04-06', 'DEF_345', 'STARTED', 500, 53.00),
                    ]

        cur.executemany(f'INSERT INTO {table_name} VALUES ({value_placeholders})', purchases)
        con.commit()

def insert(db_name, table_name, row_data):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        row = [row_data]
        cur.executemany(f'INSERT INTO {table_name} VALUES ({value_placeholders})', row)
        con.commit()

def update_status(db_name, table_name, job_id, string_status):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        # row = [row_data]
        cur.execute(f'UPDATE {table_name} SET status = \'{string_status}\' WHERE job_id = \'{job_id}\'')
        con.commit()

# def insert_value(db_name, table_name, job_id, row_data):
#     with sqlite3.connect(f'{db_name}.db') as con:
#         cur = con.cursor()

#         row = [row_data]
#         cur.execute(f'FUPDATE {table_name} WHERE \'job_id\' IS {job_id} VALUES ({value_placeholders})', row)
#         con.commit()

def find(db_name, table_name, job_id):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        res = cur.execute(f'SELECT rowid, * FROM {table_name} WHERE job_id = \'{job_id}\'')
        row = res.fetchone()
        print(str(row))
        it = iter(row)
        print(str(it))
        res_dct = dict(zip(labels, it))
        print(str(res_dct))
        # rows.append(res_dct)
        return res_dct

def list_jobs(db_name, table_name):
    rows = []

    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        print('FOUND ROWS')
        for row in cur.execute(f'SELECT rowid, * FROM {table_name} ORDER BY rowid'):
            print(row)
            it = iter(row)
            res_dct = dict(zip(labels, it))
            rows.append(res_dct)

    return rows