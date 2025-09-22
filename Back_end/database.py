import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

load_dotenv()

def get_connection():
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")  # aqui pega a variável do .env
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def test_connection():
    conn = get_connection()
    if conn:
        print("Conexão ao Supabase bem-sucedida!")
        conn.close()
    else:
        print("Falha na conexão ao banco.")

if __name__ == "__main__":
    test_connection()
