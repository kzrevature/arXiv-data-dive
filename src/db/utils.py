import os

from pg8000.native import Connection


# opens a connection to the postgres server
# user is hardcoded to the default 'postgres'
# password and url come from environ
def create_connection() -> Connection:
    db_user = "postgres"
    db_password = os.environ["ARXIN_DB_PASS"]
    db_url = os.environ["ARXIN_DB_URL"]
    conn = Connection(
        db_user,
        password=db_password,
        host=db_url,
    )
    return conn
