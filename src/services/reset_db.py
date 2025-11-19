from db.queries import create_article_table, drop_article_table
from db.utils import create_connection


# drops and recreates the Article table
# useful for development
def reset_db():
    conn = create_connection()
    drop_article_table(conn)
    create_article_table(conn)
    conn.close()
