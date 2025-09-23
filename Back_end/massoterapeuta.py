from .database import get_connection
from psycopg2 import OperationalError, DatabaseError, errors
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# -------------------------------
# Funções CRUD para Massoterapeuta
# -------------------------------

def cadastrar_massoterapeuta(nome, telefone, sexo, data_nascimento, email, senha):
    """
    Cadastra um massoterapeuta no banco e retorna o ID.
    Não permite emails duplicados.
    """
    conn = get_connection()
    if not conn:
        print("Erro: não foi possível conectar ao banco.")
        return None

    cursor = None
    try:
        cursor = conn.cursor()

        # Verifica se o email já está cadastrado
        cursor.execute("SELECT id FROM massoterapeuta WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"Erro: email '{email}' já cadastrado.")
            return None

        senha_hash = generate_password_hash(senha)
        sql = """
            INSERT INTO massoterapeuta (nome, telefone, sexo, data_nascimento, email, senha_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(sql, (nome, telefone, sexo, data_nascimento, email, senha_hash))
        massoterapeuta_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Massoterapeuta cadastrado com sucesso! ID: {massoterapeuta_id}")
        return massoterapeuta_id
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar massoterapeuta: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        conn.close()

def verificar_login(email, senha):
    """
    Verifica login do massoterapeuta.
    Retorna usuário sem senha_hash ou None se inválido.
    """
    conn = get_connection()
    usuario = None
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM massoterapeuta WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if usuario and check_password_hash(usuario['senha_hash'], senha):
                usuario.pop('senha_hash')
                return usuario
            return None
        except DatabaseError as e:
            print(f"Erro ao verificar login: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

def atualizar_conta(id, nome, telefone):
    """
    Atualiza nome e telefone do massoterapeuta.
    Email não pode ser alterado.
    """
    conn = get_connection()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            sql = "UPDATE massoterapeuta SET nome = %s, telefone = %s WHERE id = %s"
            cursor.execute(sql, (nome, telefone, id))
            conn.commit()
            print(f"Massoterapeuta {id} atualizado com sucesso!")
        except DatabaseError as e:
            conn.rollback()
            print(f"Erro ao atualizar massoterapeuta: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

def excluir_massoterapeuta(id):
    """
    Exclui um massoterapeuta do banco.
    """
    conn = get_connection()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM massoterapeuta WHERE id = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            print(f"Massoterapeuta {id} excluído com sucesso!")
        except DatabaseError as e:
            conn.rollback()
            print(f"Erro ao excluir massoterapeuta: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

# -------------------------------
# Funções de listagem
# -------------------------------

def listar_massoterapeutas():
    """
    Retorna todos os massoterapeutas.
    """
    conn = get_connection()
    massoterapeutas = []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id, nome, telefone, email FROM massoterapeuta ORDER BY nome ASC")
            massoterapeutas = cursor.fetchall()
        except DatabaseError as e:
            print(f"Erro ao buscar massoterapeutas: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return massoterapeutas

def listar_clientes():
    """
    Retorna todos os clientes.
    """
    conn = get_connection()
    clientes = []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT id, nome, telefone, email, created_at FROM cliente ORDER BY nome ASC")
            clientes = cursor.fetchall()
        except DatabaseError as e:
            print(f"Erro ao buscar clientes: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return clientes

def listar_agendamentos():
    """
    Retorna todos os agendamentos com dados do cliente.
    """
    conn = get_connection()
    agendamentos = []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT a.id, a.cliente_id, c.nome AS cliente_nome, a.massoterapeuta_id, a.data_hora, a.status, a.criado_em
                FROM agendamento a
                JOIN cliente c ON a.cliente_id = c.id
                ORDER BY a.data_hora DESC
            """)
            agendamentos = cursor.fetchall()
        except DatabaseError as e:
            print(f"Erro ao buscar agendamentos: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return agendamentos

def listar_agendamentos_massoterapeuta(massoterapeuta_id):
    """
    Retorna agendamentos de um massoterapeuta específico.
    """
    conn = get_connection()
    agendamentos = []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT a.id, a.cliente_id, c.nome AS cliente_nome, a.data_hora, a.status, a.criado_em
                FROM agendamento a
                JOIN cliente c ON a.cliente_id = c.id
                WHERE a.massoterapeuta_id = %s
                ORDER BY a.data_hora DESC
            """, (massoterapeuta_id,))
            agendamentos = cursor.fetchall()
        except DatabaseError as e:
            print(f"Erro ao buscar agendamentos do massoterapeuta: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return agendamentos
