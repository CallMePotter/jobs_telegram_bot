import psycopg2
from config import config

def insert_employee(id, name, birth_date, city_country, profession):
    sql = """INSERT INTO employee(id, name, birth_date, city_country, profession)
            VALUES(%s, %s, %s, %s, %s) RETURNING id"""
    conn = None
    try:
        print("Connecting to database...")

        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print("Connection sucessful")

        print("Exectuting commands")
        cur.execute(sql, (id, name, birth_date, city_country, profession))
        id = cur.fetchone()[0]
        conn.commit()
        print("Operation successful")

        print("Closing connection")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            print("Closing connection")
            conn.close()

    return id


if __name__ == '__main__':
    insert_employee(1, 'Dmitriy', '06.04.2003', 'Yekaterinburg, Russia', 'programmer')