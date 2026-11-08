
import psycopg

with psycopg.connect(
    dbname="supportai_db",
    user="macbookpro",
    host="localhost",
    port=5432
) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, email FROM users;")
        users = cur.fetchall()

        for user in users:
            print(user)
