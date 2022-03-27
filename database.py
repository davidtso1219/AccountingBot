import os, psycopg2
from utils import get_args

URI = os.getenv('DATABASE_URL')

def query(command, args=None):
    try:
        connection = psycopg2.connect(URI)
        with connection:
            cursor = connection.cursor()
            cursor.execute(command, args)

            try:
                data = cursor.fetchall()
            except psycopg2.ProgrammingError:
                data = None

            connection.commit()

    except psycopg2.Error as e:
        print(f'Had problem connecting with error {e}.')
        raise ValueError('Could not connect to database')

    finally:

        if connection:
            connection.rollback()

        if data:
            return data

def add_expense(**info):
    '''
    price, month, day, year, cat, det, name
    '''
    command = 'INSERT INTO records (price, month, day, year, name, category, detail) VALUES (%s, %s, %s, %s, %s, %s, %s);'
    columns = ['price', 'month', 'day', 'year', 'name', 'cat', 'det']
    args = get_args(info, columns)
    query(command, args)

def total(**info):
    '''
    month, day, year, name
    '''
    if info['day']:
        command = 'SELECT SUM(price) FROM records WHERE month = %s AND day = %s AND year = %s AND name = %s;'
        columns = ['month', 'day', 'year', 'name']
    else:
        command = 'SELECT SUM(price) FROM records WHERE month = %s AND year = %s AND name = %s;'
        columns = ['month', 'year', 'name']

    args = get_args(info, columns)
    data = query(command, args)
    sum_price = data[0][0] if data[0][0] else 0
    return sum_price

def create():
    command = "DROP TABLE IF EXISTS records"
    query(command)
    command = '''create table records (
    _id serial primary key,
    price float,
    month int,
    day int,
    year int,
    name varchar(10),
    category varchar(20),
    detail varchar(100)
    );
    '''
    query(command)
