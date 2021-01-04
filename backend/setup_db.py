import sqlite3


def init_db(name):
    conn = sqlite3.connect(name)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS labs (
                id VARCHAR(64) PRIMARY KEY,
                name VARCHAR(64),
                worker_id INT,
                user_id INT,
                created_date DATETIME,
                lab_template_id INT,
                start_date DATETIME,
                expiration_date DATETIME,
                description VARCHAR (128),
                vm_count INT
              )""")
    c.execute("""CREATE TABLE IF NOT EXISTS workers (
                id VARCHAR(64) PRIMARY KEY,
                state INT,
                host VARCHAR(64),
                port VARCHAR(5),
                last_updated DATETIME
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
    init_db('vlab.db')
