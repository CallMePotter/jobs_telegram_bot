import psycopg2
from config import config

def create_table():
    # Create tables in database
    commands = (
        """
        CREATE TABLE employee (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            city_country VARCHAR(255) NOT NULL,
            profession VARCHAR(255) NOT NULL
        ) 
        """,
        """
        CREATE TABLE business (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """)
    conn = None
    try:
        print("Connecting to database...")

        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print("Connected successfully")

        for command in commands:
            print(command)
            cur.execute(command)

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            print("Closing connection...")
            conn.close()

if __name__ == '__main__':
    create_table()