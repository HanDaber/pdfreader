import sqlite3

db_name = 'TEST_DB_1'
table_name = 'artifacts_table_1'

labels = ['row_id', 'job_id',        'pdf_location',  'images_location', 'analysis_location', 'crops_location']
types = ['INTEGER', 'TEXT NOT NULL', 'TEXT',          'TEXT',            'TEXT',              'TEXT']
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

def insert(row_data):
    with sqlite3.connect(f'{db_name}.db') as con:
        cur = con.cursor()

        row = [row_data]
        cur.executemany(f'INSERT INTO {table_name} VALUES ({value_placeholders})', row)
        con.commit()
