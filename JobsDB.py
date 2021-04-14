import sqlite3

db_name = 'TEST_DB_1'
table_name = 'jobs_table_1'

labels = ['row_id', 'date', 'job_id',               'status', 'qty', 'price']
types = ['INTEGER', 'TEXT', 'TEXT NOT NULL UNIQUE', 'TEXT', 'REAL', 'REAL']
value_placeholders = '?,?,?,?,?'

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

        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

def hydrate():
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        purchases = [('2006-03-28', 'ABC_123', 'PENDING', 1000, 45.00),
                    ('2006-04-05', 'CDE_234', 'PENDING', 1000, 72.00),
                    ('2006-04-06', 'DEF_345', 'STARTED', 500, 53.00),
                    ]

        cur.executemany(f'INSERT INTO {table_name} VALUES ({value_placeholders})', purchases)
        con.commit()

def insert(row_data):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        row = [row_data]
        cur.executemany(f'INSERT INTO {table_name} VALUES ({value_placeholders})', row)
        con.commit()

def update_status(job_id, string_status):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        # row = [row_data]
        cur.execute(f'UPDATE {table_name} SET status = \'{string_status}\' WHERE job_id = \'{job_id}\'')
        con.commit()

# def insert_value(, job_id, row_data):
#     with sqlite3.connect(f'{db_name}.db') as con:
#         cur = con.cursor()

#         row = [row_data]
#         cur.execute(f'FUPDATE {table_name} WHERE \'job_id\' IS {job_id} VALUES ({value_placeholders})', row)
#         con.commit()

# ls -U mounted_doc_man/File2/715.pdf | head -1

def find(job_id):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        res = cur.execute(f'SELECT rowid, * FROM {table_name} WHERE job_id = \'{job_id}\'')
        row = res.fetchone()
        # print(str(row))
        it = iter(row)
        # print(str(it))
        res_dct = dict(zip(labels, it))
        # print(str(res_dct))
        # rows.append(res_dct)
        return res_dct

def list_jobs():
    rows = []

    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        # print('FOUND ROWS')
        for row in cur.execute(f'SELECT rowid, * FROM {table_name} ORDER BY rowid'):
            # print(row)
            it = iter(row)
            res_dct = dict(zip(labels, it))
            rows.append(res_dct)

    return rows

# def list_jobs_with_values(values_table):
#     rows = []

#     with sqlite3.connect(f'{db_name}.db') as con:
#         cur = con.cursor()

#         print('FOUND ROWS')
#         for row in cur.execute(f'SELECT * FROM {table_name} INNER JOIN {values_table} ON {table_name}.job_id = {values_table}.job_id'):
#             print(row)
#             it = iter(row)
#             res_dct = dict(zip(labels, it))
#             rows.append(res_dct)

#     return rows