import psycopg2
import sys


def create_db(host, db, user, password):
    conn = psycopg2.connect(host=host, user=user, password=password)
    conn.autocommit = True
    c = conn.cursor()
    c.execute("CREATE DATABASE " + db)
    conn.close()


def init_db(host, db, user, password):
    conn = psycopg2.connect(host=host, database=db, user=user, password=password)
    print("Connected!")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS labs (
                id VARCHAR(64) PRIMARY KEY,
                name VARCHAR(64),
                worker_id VARCHAR(64),
                user_id INT,
                created_date TIMESTAMP,
                lab_template_id INT,
                start_date TIMESTAMP,
                expiration_date TIMESTAMP,
                description VARCHAR (128),
                vm_count INT
              )""")
    c.execute("""CREATE TABLE IF NOT EXISTS workers (
                id VARCHAR(64) PRIMARY KEY,
                state INT,
                host VARCHAR(64),
                port VARCHAR(5),
                last_updated TIMESTAMP
              )""")
    c.execute("""CREATE TABLE IF NOT EXISTS machines (
                id VARCHAR(64) PRIMARY KEY,
                lab_id VARCHAR(64),
                default_name VARCHAR(64),
                display_name VARCHAR(64)
            )""")
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                username VARCHAR(64),
                password_hash VARCHAR(64),
                email VARCHAR(64)
              )""")
    c.execute("""INSERT INTO users VALUES (1, 'user1', '$2y$12$XSjsdOLKBCIKHQ78j8D5L.DGCI0j5BXFYsZRgidZFDUxyi.r/Bn46', 'email')
    """)
    c.execute("""CREATE TABLE IF NOT EXISTS lab_templates(
                    id INT PRIMARY KEY,
                    code_name VARCHAR(64),
                    lab_name VARCHAR(64)
                )""")
    c.execute("""INSERT INTO lab_templates VALUES (1, 'BASE', 'Base')""")
    c.execute("""INSERT INTO lab_templates VALUES (2, 'KATHARA', 'Kathara')""")
    c.execute("""INSERT INTO lab_templates VALUES (3, 'KATHARA_CONTAINER', 'Kathara (Container)')""")
    c.execute("""INSERT INTO lab_templates VALUES (4, 'P4', 'P4Lang')""")
    c.execute("""INSERT INTO lab_templates VALUES (5, 'RSTUDIO', 'RStudio')""")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("USAGE: setup.py <address> <db_name> <user> <password>")
    # create_db('localhost', 'vlab', 'postgres', 'test_database_password')
    # init_db('localhost', 'vlab', 'postgres', 'test_database_password')
    init_db(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
