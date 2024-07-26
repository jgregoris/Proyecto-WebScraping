import psycopg2

class Database:
    def __init__(self, dbname, user, password, host, port):
        # Constructor de la clase Database. Establece la conexión con la base de datos PostgreSQL.
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def close(self):
        # Cierra la conexión con la base de datos.
        self.conn.close()

    def insert_author(self, author_name, author_info):
        # Inserta o actualiza un autor en la base de datos.
        # Si el autor ya existe (basado en el nombre), actualiza su información.
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
            return cur.fetchone()[0] # Retorna el ID del autor insertado.

    def insert_quote(self, text, author_id):
        # Inserta una nueva cita en la base de datos.
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO quotes (text, author_id)
                VALUES (%s, %s)
                RETURNING id
            """, (text, author_id))
            return cur.fetchone()[0] # Retorna el ID de la cita insertada.

    def insert_tag(self, tag_name):
        # Inserta o actualiza una etiqueta en la base de datos.
        # Si la etiqueta ya existe, no hace nada (debido a ON CONFLICT).
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO tags (name)
                VALUES (%s)
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                RETURNING id
            """, (tag_name,))
            return cur.fetchone()[0] # Retorna el ID de la etiqueta insertada o existente

    def insert_quote_tag(self, quote_id, tag_id):
        # Asocia una etiqueta con una cita en la tabla de relación quotes_tags.
        # Si la relación ya existe, no hace nada (debido a ON CONFLICT).
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO quotes_tags (quote_id, tag_id)
                VALUES (%s, %s)
                ON CONFLICT (quote_id, tag_id) DO NOTHING
            """, (quote_id, tag_id))

    def commit(self):
        # Confirma los cambios en la base de datos.
        self.conn.commit()

    def rollback(self):
        # Revierte los cambios en la base de datos en caso de error.
        self.conn.rollback()