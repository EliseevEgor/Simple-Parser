import psycopg2

con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="secret",
    host="localhost",
    port="5432"
)

cur = con.cursor()

"""
Создает базу данных
_______________________________________________
| ID пользователя Telegram | Название компании|
"""


def create_table(table):
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS {}  
           (ID INT NOT NULL,
           COMPANY_NAME TEXT NOT NULL,
           PRIMARY KEY(ID, COMPANY_NAME));'''.format(table))
    except psycopg2.Error as e:
        cur.execute('''ROLLBACK''')
        con.commit()
        return "Ой-ёй, что-то пошло не так"

    con.commit()


"""
Добавляет новую компанию
Если все получилось - возвращает пользователю строку Компания добавлена
Если такая компания есть - 
Иначе - возврашает ошибку 
"""


def add_company(user_id: int, name: str, table: str):
    try:
        if name.islower():
            name = name.capitalize()
        cur.execute('''INSERT INTO {} (ID, COMPANY_NAME) VALUES ({}, '{}');'''.format(table, user_id, name))
        con.commit()
    except psycopg2.Error as e:
        cur.execute('''ROLLBACK''')
        con.commit()
        if e.pgcode == '23505':
            return "Такая компания уже есть"
        return "Ой-ёй, что-то пошло не так"
    return "Компания {} добавлена".format(name)


"""
Удаляет компанию
Если получилось - Компания удалена
Если такой компании нет - 
Иначе - ошибка
"""


def delete_company(user_id: int, name: str, table: str):
    try:
        if name.islower():
            name = name.capitalize()
        cur.execute('''DELETE FROM {} WHERE ID={} AND COMPANY_NAME='{}';'''.format(table, user_id, name))
        con.commit()
    except psycopg2.Error as e:
        cur.execute('''ROLLBACK''')
        con.commit()
        # if e.pgcode == psycopg2.errorcodes:
        #     return "Такой компании у Вас нет"
        return "Ой-ёй, что-то пошло не так"
    return "Компания {} удалена".format(name)


"""
Показывает информацию о избранных компаниях определенного пользователя
Если компании есть - возвращает их
Если компаний нет - у вас пока что нет изранных компаний
Иначе -
"""


def get_companies(user_id: int, table: str):
    try:
        cur.execute('''SELECT COMPANY_NAME from {} where ID={}'''.format(table, user_id))
        con.commit()
    except psycopg2.Error as e:
        cur.execute('''ROLLBACK''')
        con.commit()

        print(e.pgcode)
        return "Ой-ёй, что-то пошло не так"

    rows = cur.fetchall()
    if len(rows) == 0:
        return "у вас пока что нет изранных компаний"
    result = "Ваши компании: \n"

    for row in rows:
        result += str(row[0] + ",\n")

    result = result[:-2]
    return result


def drop_table(table: str):
    try:
        cur.execute('''DROP TABLE {};'''.format(table))
        con.commit()
    except psycopg2.Error:
        cur.execute('''ROLLBACK''')
        con.commit()
