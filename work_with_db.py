import os
import logging
import psycopg2
from dotenv import load_dotenv


load_dotenv()

host_db = os.getenv('HOST_DB')
pass_db = os.getenv('PASS_DB')
port_db = os.getenv('PORT_DB')
user_db = os.getenv('USER_DB')
database = os.getenv('NAME_DB')


def select_in_emails():
    connection = None

    try:
        connection = psycopg2.connect(user=user_db,
                                      password=pass_db,
                                      host=host_db,
                                      port=port_db,
                                      database=database)

        cursor = connection.cursor()
        cursor.execute("SELECT id, email FROM emails;")
        data = cursor.fetchall()
        logging.info("Команда успешно выполнена")
        str_emails = ''
        for i in range(len(data)):
            str_emails += f'{data[i][0]}. {data[i][1]}\n'
        return str_emails
    except (Exception, psycopg2.Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        return None
    finally:
        if connection is not None:
            cursor.close()
            connection.close()


def insert_in_emails(user_text):
    list_from_user_text = user_text.split()
    connection = None
    try:
        connection = psycopg2.connect(user=user_db,
                                      password=pass_db,
                                      host=host_db,
                                      port=port_db,
                                      database=database)
        for i in range(1, len(list_from_user_text), 2):
            email = list_from_user_text[i]
            email = str(email)
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO emails (email) 
            VALUES (%s);
            """,
                           (email,))
            connection.commit()
            logging.info("Команда успешно выполнена")
            return 'Данные записаны'
    except (Exception, psycopg2.Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        return 'Произошла ошибка при записи'
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            logging.info("Соединение с PostgreSQL закрыто")


def select_in_phonenumbers():
    connection = None

    try:
        connection = psycopg2.connect(user=user_db,
                                      password=pass_db,
                                      host=host_db,
                                      port=port_db,
                                      database=database)

        cursor = connection.cursor()
        cursor.execute("SELECT id, phonenumber FROM phonenubmers;")
        data = cursor.fetchall()
        logging.info("Команда успешно выполнена")
        str_phonenumbers = ''
        for i in range(len(data)):
            str_phonenumbers += f'{data[i][0]}. {data[i][1]}\n'
        return str_phonenumbers
    except (Exception, psycopg2.Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        return None
    finally:
        if connection is not None:
            cursor.close()
            connection.close()


def insert_in_phonenumbers(user_text):
    list_from_user_text = user_text.split()
    connection = None
    try:
        connection = psycopg2.connect(user=user_db,
                                      password=pass_db,
                                      host=host_db,
                                      port=port_db,
                                      database=database)

        cursor = connection.cursor()
        for i in range(1, len(list_from_user_text), 2):
            phonenumber = list_from_user_text[i]
            cursor.execute("""
            INSERT INTO phonenubmers (phonenumber) 
            VALUES (%s);
            """,
                           (phonenumber,))
            connection.commit()
            logging.info("Команда успешно выполнена")
            return 'Данные записаны'
    except (Exception, psycopg2.Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        return 'Произошла ошибка при записи'
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            logging.info("Соединение с PostgreSQL закрыто")


def main():
    k = select_in_emails()
    print(k)
    c = select_in_phonenumbers()
    print(c)

if __name__ == '__main__':
    main()

