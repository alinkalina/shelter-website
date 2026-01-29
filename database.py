import sqlite3


def open_db():
    con = sqlite3.connect('shelter.db', check_same_thread=False)
    cur = con.cursor()
    return con, cur


def create_tables():
    connection, cursor = open_db()

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS animals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_type TEXT NOT NULL,
        name TEXT NOT NULL,
        birth_year INTEGER DEFAULT 0,
        state INTEGER DEFAULT 1
    );
    ''')
    # state - 1 - питомец находится в приюте, 2 - питомец обрёл хозяев

    cursor.close()
    connection.commit()
    connection.close()


create_tables()


def get_from_db(sql: str) -> list[tuple]:
    connection, cursor = open_db()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def add_animal(animal_type: str, name: str, birth_year: int, state: int):
    connection, cursor = open_db()
    sql = f'INSERT INTO animals (animal_type, name, birth_year, state) VALUES (?, ?, ?, ?);'
    try:
        cursor.execute(sql, (animal_type, name, birth_year, state))
    except sqlite3.IntegrityError:
        pass
    finally:
        connection.commit()
        cursor.close()
        connection.close()


def get_all_animals():
    sql = f'SELECT * FROM animals;'
    result = get_from_db(sql)
    return result
