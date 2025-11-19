from pg8000.native import Connection


# drops Article table
def drop_article_table(conn: Connection):
    QUERY_STR = "DROP TABLE IF EXISTS Article;"
    conn.run(QUERY_STR)


# creates Article table with the columns shown below
def create_article_table(conn: Connection):
    QUERY_STR = (
        "CREATE TABLE Article ("
        "   id             VARCHAR(20) PRIMARY KEY,"
        "   title          VARCHAR(255),"
        "   created_at     TIMESTAMP,"
        "   updated_at     TIMESTAMP"
        ");"
    )
    conn.run(QUERY_STR)
