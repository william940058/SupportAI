import psycopg


def get_connection():
    return psycopg.connect(
        dbname="supportai_db",
        user="macbookpro",
        host="localhost",
        port=5432
    )
