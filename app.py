import streamlit as st
import pandas as pd
from database import Database
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Función para obtener todas las citas de la base de datos
def get_all_quotes():
    db = Database(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    with db.conn.cursor() as cur:
        cur.execute("""
            SELECT q.id, q.text, a.name as author, a.bio, a.born_date, a.born_location,
                   string_agg(t.name, ', ') as tags
            FROM quotes q
            JOIN authors a ON q.author_id = a.id
            LEFT JOIN quotes_tags qt ON q.id = qt.quote_id
            LEFT JOIN tags t ON qt.tag_id = t.id
            GROUP BY q.id, q.text, a.name, a.bio, a.born_date, a.born_location
        """)
        columns = [desc[0] for desc in cur.description]
        quotes = [dict(zip(columns, row)) for row in cur.fetchall()]
    db.close()
    return quotes

# Configuración de la página de Streamlit
st.set_page_config(page_title="Visualizador de Citas", layout="wide")

# Cambiar el color de fondo a naranja claro
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFE4B5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título de la aplicación
st.title("Visualizador de Citas")

# Obtener todas las citas
quotes = get_all_quotes()

# Convertir las citas a un DataFrame de pandas
df = pd.DataFrame(quotes)

# Mostrar todas las citas en una tabla
st.header("Todas las Citas")
st.dataframe(df)

# Permitir al usuario buscar citas por autor
st.header("Buscar Citas por Autor")
author = st.selectbox("Selecciona un autor", options=sorted(df['author'].unique()))
author_quotes = df[df['author'] == author]

if not author_quotes.empty:
    # Mostrar información biográfica del autor
    st.subheader(f"Sobre {author}")
    author_info = author_quotes.iloc[0]
    st.write(f"Biografía: {author_info['bio']}")
    st.write(f"Fecha de nacimiento: {author_info['born_date']}")
    st.write(f"Lugar de nacimiento: {author_info['born_location']}")

    # Mostrar las citas del autor
    st.subheader(f"Citas de {author}")
    for _, quote in author_quotes.iterrows():
        st.write(f"'{quote['text']}'")
        st.write(f"Tags: {quote['tags']}")
        st.write("---")
else:
    st.write("No se encontraron citas para este autor.")