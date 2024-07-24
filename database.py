import psycopg2

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def close(self):
        self.conn.close()

    def insert_author(self, author_name, author_info):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO authors (name, bio, born_date, born_location)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                SET bio = EXCLUDED.bio,
                    born_date = EXCLUDED.born_date,
                    born_location = EXCLUDED.born_location
                RETURNING id
            """, (author_name, author_info['bio'], author_info['born_date'], author_info['born_location']))
            return cur.fetchone()[0]

    def insert_quote(self, text, author_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO quotes (text, author_id)
                VALUES (%s, %s)
                RETURNING id
            """, (text, author_id))
            return cur.fetchone()[0]

    def insert_tag(self, tag_name):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tags (name)
                VALUES (%s)
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                RETURNING id
            """, (tag_name,))
            return cur.fetchone()[0]

    def insert_quote_tag(self, quote_id, tag_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO quotes_tags (quote_id, tag_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (quote_id, tag_id))

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()