import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(20),
            lastname VARCHAR(20),
            email VARCHAR(40) NOT NULL,
            phones TEXT);
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES clients(id),
            phones VARCHAR(20) NOT NULL);
        """)
        conn.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    if first_name == None or last_name == None or email == None:
        print('Не заполнено основное поле Имя/Фамилия/Почта')
        return

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(firstname, lastname, email, phones) VALUES(%s, %s, %s, %s) RETURNING firstname, lastname;
            """, (first_name, last_name, email, phones))
        print('Добавили клиента ', cur.fetchone())

def get_phones(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT phones FROM clients WHERE id=%s;
            """, (client_id))
        phones = cur.fetchall()[0][0]
        return phones

def add_phone(conn, client_id, phone):
    phones = get_phones(conn, client_id)
    phones = (phone, str(phones) + ',' + phone)[phones != None]
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients SET phones=%s WHERE id=%s
            """, (phones, client_id))
        cur.execute("""
            SELECT * FROM clients WHERE id=%s;
            """, (client_id))
        cur.fetchall()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
                UPDATE clients SET firstname=%s WHERE id=%s
                """, (first_name, client_id))
        if last_name is not None:
            cur.execute("""
                UPDATE clients SET lastname=%s WHERE id=%s
                """, (last_name, client_id))
        if email is not None:
            cur.execute("""
                UPDATE clients SET email=%s WHERE id=%s
                """, (email, client_id))
        if phone is not None:
            phones = get_phones(conn, client_id)
            phones = (phone, str(phones) + ',' + phone)[phones != None]
            cur.execute("""
                UPDATE clients SET phones=%s WHERE id=%s
                """, (phones, client_id))
        cur.execute("""
            SELECT * FROM clients WHERE id=%s;
            """, (client_id,))
        print(cur.fetchall())

def delete_phone(conn, client_id, phone):
    # предполагается, что пишут удаляемы телефон точно в таком формате, как он был туда записан :D
    # сорри, заскакиываю со сдачей дз в последний вагон...
    phones = get_phones(conn, client_id)
    phones_list = phones.split(',')
    if phone in phones_list:
        phones_list.remove(phone)
    else:
        print('Телефон не найден ', phone)
        return
    phones = ','.join(phones_list)
    print(phones)
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients SET phones=%s WHERE id=%s
            """, (phones, client_id))
        cur.execute("""
            SELECT * FROM clients WHERE id=%s;
            """, (client_id,))
        print(cur.fetchall())


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clients WHERE id=%s;
            """, (client_id,))
        cur.execute("""
            SELECT * FROM clients;
            """)
        print(cur.fetchall())


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM clients 
            WHERE firstname=%s OR lastname=%s OR email=%s OR phones LIKE %s;
            """, (first_name, last_name, email, '%'+str(phone)+'%'))
        print(cur.fetchall())




def all_clients(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM clients;
            """)
        print(cur.fetchall())


with psycopg2.connect(database="netology_clients_db", user="postgres", password="@Y2r0yl2GUflvby") as conn:
    # create_db(conn)

    # add_client(conn, 'Иван', 'Иванов', 'iivanov@gmail.com', '+79818474738')
    # add_client(conn, 'Мария', 'Сазонова', 'saz1212@gmail.com')
    # add_client(conn, 'Кристиан', 'Белозубиков', 'cris666@gmail.com', '+79263452323, 455-23-33')
    # add_client(conn, 'Вася', None, None)
    # add_client(conn, 'Нина', 'Креветко', None)
    # add_client(conn, 'Максим', 'Иванов', 'iii@gmail.com')
    #
    # all_clients(conn)
    #
    # add_phone(conn, '2', '234-45-45')
    # add_phone(conn, '1', '777-45-34')
    #
    # all_clients(conn)
    #
    # change_client(conn, '1', 'Семен')
    # change_client(conn, '2', None, 'Логозина')
    # change_client(conn, '3', None, None, 'belozub@gmail.com')
    # change_client(conn, '2', None, None, None, '+7-999-345-76-76')
    #
    # all_clients(conn)
    #
    # delete_phone(conn, '1', '777-45-33')
    # delete_phone(conn, '1', '777-45-34')
    #
    # all_clients(conn)
    #
    # find_client(conn, 'Мария')
    # find_client(conn, None, 'Иванов')
    # find_client(conn, None, None, 'belozub@gmail.com')
    # find_client(conn, None, None, None, '234-45-45')
    #
    # delete_client(conn, 6)

conn.close()