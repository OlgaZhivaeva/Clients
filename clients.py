import psycopg2
from password import PASS

def get_id(cur, email):
    """Функция определяет id клиента по е-майл"""
    cur.execute("""
    SELECT client_id FROM client WHERE email=%s;""", (email,))
    return cur.fetchone()[0]

def create_table(cur):
    """Функция создает таблицы для базы данных"""
    cur.execute("""
    CREATE TABLE client(
        client_id SERIAL PRIMARY KEY,
        name VARCHAR(40)  NOT NULL,
        surname VARCHAR(40)  NOT NULL,
        email VARCHAR(40) UNIQUE NOT NULL);
    CREATE TABLE telephone(
        telephone_id SERIAL PRIMARY KEY,
        number VARCHAR(20) NOT NULL,
        client_id INTEGER REFERENCES client(client_id)); """)

def add_client(cur, first_name, last_name, email, phones=[]):
    """Функция добавляет клиента в базу данных"""
    cur.execute("""
    INSERT INTO client (name, surname, email)
    VALUES (%s, %s, %s);""", (first_name, last_name, email ))
    add_phone(cur, get_id(cur, email), phones)

def add_phone(cur, client_id, phones:list):
    """Функция добавляет номера телефонов клиента в базу данных """
    for phone in phones:
        cur.execute("""
        INSERT INTO telephone (number, client_id)
        VALUES (%s, %s);""", (phone, client_id))

def change_client(cur, client_id, first_name=None, last_name=None, email=None, phones=[]):
    """Функция вносит изменетия в данные о клиенте"""
    if first_name != None:
        cur.execute("""
        UPDATE client SET name=%s WHERE client_id=%s;""",(first_name, client_id))
    if last_name != None:
        cur.execute("""
        UPDATE client SET surname=%s WHERE client_id=%s;""",(last_name, client_id))
    if email != None:
        cur.execute("""
        UPDATE client SET email=%s WHERE client_id=%s;""",(email, client_id))
    if phones != []:
        cur.execute("""
        DELETE FROM telephone WHERE client_id=%s;""",(client_id,))
        add_phone(cur, client_id, phones)

def delete_phone(cur, client_id, phones:list):
    """Функция удаляет номера телефонов клиента"""
    for phone in phones:
        cur.execute("""
        DELETE FROM telephone WHERE client_id=%s;""", (client_id,))

def delete_client(cur, client_id):
    """Функция удаляет клиента из базы данных"""
    cur.execute("""
    DELETE FROM telephone WHERE client_id=%s;""", (client_id,))
    cur.execute("""
    DELETE FROM client WHERE client_id=%s;""", (client_id,))

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    """Функция осуществляет поиск клиента по его данным"""
    cur.execute("""
    SELECT c.client_id, name, surname, email, number FROM client c
    LEFT JOIN telephone t ON c.client_id = t.client_id
    WHERE name=%s OR surname=%s OR email=%s OR number=%s;""", (first_name, last_name, email, phone))
    print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="test", user="postgres", password=PASS) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE telephone;
            DROP TABLE client;
            """)
            create_table(cur)
            add_client(cur, 'Евгений', 'Сотников', 'bumer@mail.ru', ['+79527797077', '42616'])
            add_client(cur, 'Ольга', 'Живаева', 'olga.zhiv@yandex.ru')
            add_client(cur, 'Алена', 'Баринова', 'al89@mail.ru', ['89101364555', '423212', '423345'])
            add_client(cur, 'Альберт', 'Ванян', 'AlV@mail.ru', ['89519144747', '89200324444', '422225','4322226'])
            add_client(cur, 'Дмитрий', 'Смирнов', 'smirnov75@yandex.ru', ['411726'])
            add_client(cur, 'Александр', 'Смирнов', 'smirnov73@yandex.ru')
            add_phone(cur, get_id(cur, 'smirnov73@yandex.ru'), ['89202573211', '411726'])
            change_client(cur, get_id(cur, 'bumer@mail.ru'), 'Yevgeniy', 'Sotnikov')
            delete_phone(cur, get_id(cur, 'bumer@mail.ru'), ['42616', '+79527797077'])
            change_client(cur, get_id(cur, 'al89@mail.ru'), email='al.bar89@mail.ru', phones=['+79101364555', '+79201583433'])
            delete_client(cur, get_id(cur, 'AlV@mail.ru'))
            find_client(cur, last_name='Смирнов')
            find_client(cur, 'Ольга')