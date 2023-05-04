import psycopg2
from config import config

def connect():
    conn = None
    try:
        # read config
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create cursor
        cur = conn.cursor()

        # Exec a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # Display info
        db_version = cur.fetchone()
        print(db_version)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()