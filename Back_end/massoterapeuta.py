# ===== IMPORTS NECESSÁRIOS =====
from .database import get_connection  # Função para conectar ao banco PostgreSQL
from psycopg2 import OperationalError, DatabaseError, errors  # Drivers PostgreSQL e tratamento de erros
from psycopg2.extras import RealDictCursor  # Cursor que retorna dados como dicionário
from werkzeug.security import check_password_hash, generate_password_hash  # Criptografia de senhas
from datetime import datetime  # Manipulação de datas e horários

# -------------------------------
# Funções CRUD para Massoterapeuta
# -------------------------------

def cadastrar_massoterapeuta(nome, telefone, sexo, data_nascimento, email, senha):
    """
    Cadastra um massoterapeuta no banco e retorna o ID.
    Não permite emails duplicados.
    """
    conn = get_connection()  # Conecta ao banco de dados
    if not conn:  # Se não conseguir conectar
        print("Erro: não foi possível conectar ao banco.")
        return None

    cursor = None  # Inicializa cursor
    try:  # Tenta executar
        cursor = conn.cursor()  # Cria cursor para executar comandos SQL

        # Verifica se o email já está cadastrado
        cursor.execute("SELECT id FROM massoterapeuta WHERE email = %s", (email,))  # Busca email no banco
        if cursor.fetchone():  # Se encontrou email
            print(f"Erro: email '{email}' já cadastrado.")
            return None

        senha_hash = generate_password_hash(senha)  # Criptografa a senha
        sql = """
            INSERT INTO massoterapeuta (nome, telefone, sexo, data_nascimento, email, senha_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """  # SQL para inserir massoterapeuta e retornar o ID
        cursor.execute(sql, (nome, telefone, sexo, data_nascimento, email, senha_hash))  # Executa insert
        massoterapeuta_id = cursor.fetchone()[0]  # Pega o ID retornado
        conn.commit()  # Confirma a transação no banco
        print(f"Massoterapeuta cadastrado com sucesso! ID: {massoterapeuta_id}")
        return massoterapeuta_id  # Retorna o ID do massoterapeuta
    except Exception as e:  # Se der erro
        conn.rollback()  # Desfaz alterações
        print(f"Erro ao cadastrar massoterapeuta: {e}")
        return None  # Retorna nulo
    finally:  # Sempre executa
        if cursor:  # Se cursor existe
            cursor.close()  # Fecha cursor
        conn.close()  # Fecha conexão

def verificar_login(email, senha):
    """
    Verifica login do massoterapeuta.
    Retorna usuário sem senha_hash ou None se inválido.
    """
    conn = get_connection()  # Conecta ao banco
    usuario = None  # Inicializa usuário
    if conn:  # Se conectou
        cursor = None  # Inicializa cursor
        try:  # Tenta executar
            cursor = conn.cursor(cursor_factory=RealDictCursor)  # Cursor que retorna dict
            cursor.execute("SELECT * FROM massoterapeuta WHERE email = %s", (email,))  # Busca por email
            usuario = cursor.fetchone()  # Pega o usuário
            if usuario and check_password_hash(usuario['senha_hash'], senha):  # Se existe e senha confere
                usuario.pop('senha_hash')  # Remove senha do retorno
                return usuario  # Retorna usuário sem senha
            return None  # Login inválido
        except DatabaseError as e:  # Se der erro no banco
            print(f"Erro ao verificar login: {e}")
            return None  # Retorna nulo
        finally:  # Sempre executa
            if cursor:  # Se cursor existe
                cursor.close()  # Fecha cursor
            conn.close()  # Fecha conexão

def atualizar_conta(id, nome, telefone):
    """
    Atualiza nome e telefone do massoterapeuta.
    Email não pode ser alterado.
    """
    conn = get_connection()  # Conecta ao banco
    if conn:  # Se conectou
        cursor = None  # Inicializa cursor
        try:  # Tenta executar
            cursor = conn.cursor()  # Cria cursor
            sql = "UPDATE massoterapeuta SET nome = %s, telefone = %s WHERE id = %s"  # SQL update
            cursor.execute(sql, (nome, telefone, id))  # Executa update
            conn.commit()  # Confirma alteração
            print(f"Massoterapeuta {id} atualizado com sucesso!")
        except DatabaseError as e:  # Se der erro
            conn.rollback()  # Desfaz alterações
            print(f"Erro ao atualizar massoterapeuta: {e}")
        finally:  # Sempre executa
            if cursor:  # Se cursor existe
                cursor.close()  # Fecha cursor
            conn.close()  # Fecha conexão

def excluir_massoterapeuta(id):
    """
    Exclui um massoterapeuta do banco.
    """
    conn = get_connection()  # Conecta ao banco
    if conn:  # Se conectou
        cursor = None  # Inicializa cursor
        try:  # Tenta executar
            cursor = conn.cursor()  # Cria cursor
            sql = "DELETE FROM massoterapeuta WHERE id = %s"  # SQL para deletar
            cursor.execute(sql, (id,))  # Executa delete
            conn.commit()  # Confirma exclusão
            print(f"Massoterapeuta {id} excluído com sucesso!")
        except DatabaseError as e:  # Se der erro
            conn.rollback()  # Desfaz alterações
            print(f"Erro ao excluir massoterapeuta: {e}")
        finally:  # Sempre executa
            if cursor:  # Se cursor existe
                cursor.close()  # Fecha cursor
            conn.close()  # Fecha conexão

# ===== FUNÇÕES DE LISTAGEM =====

def listar_massoterapeutas():
    """
    Retorna todos os massoterapeutas.
    """
    conn = get_connection()  # Conecta ao banco
    massoterapeutas = []  # Lista vazia
    if conn:  # Se conectou
        cursor = None  # Inicializa cursor
        try:  # Tenta executar
            cursor = conn.cursor(cursor_factory=RealDictCursor)  # Cursor que retorna dict
            cursor.execute("SELECT id, nome, telefone, email FROM massoterapeuta ORDER BY nome ASC")  # Busca todos
            massoterapeutas = cursor.fetchall()  # Pega todos os resultados
        except DatabaseError as e:  # Se der erro
            print(f"Erro ao buscar massoterapeutas: {e}")
        finally:  # Sempre executa
            if cursor:  # Se cursor existe
                cursor.close()  # Fecha cursor
            conn.close()  # Fecha conexão
    return massoterapeutas  # Retorna lista

def listar_clientes():
    """
    Retorna todos os clientes.
    """
    conn = get_connection()  # Conecta ao banco
    clientes = []  # Lista vazia
    if conn:  # Se conectou
        cursor = None  # Inicializa cursor
        try:  # Tenta executar
            cursor = conn.cursor(cursor_factory=RealDictCursor)  # Cursor que retorna dict
            cursor.execute("SELECT id, nome, telefone, email, created_at FROM cliente ORDER BY nome ASC")  # Busca clientes
            clientes = cursor.fetchall()  # Pega todos os resultados
        except DatabaseError as e:  # Se der erro
            print(f"Erro ao buscar clientes: {e}")
        finally:  # Sempre executa
            if cursor:  # Se cursor existe
                cursor.close()  # Fecha cursor
            conn.close()  # Fecha conexão
    return clientes  # Retorna lista

def listar_agendamentos():
    """
    Retorna todos os agendamentos com dados do cliente.
    """
    conn = get_connection()  # Conecta ao banco
    agendamentos = []  # Lista vazia
    if conn:  # Se conectou
        cursor = None  # Inicializa cursor
        try:  # Tenta executar
            cursor = conn.cursor(cursor_factory=RealDictCursor)  # Cursor que retorna dict
            cursor.execute("""
                SELECT a.id, a.cliente_id, c.nome AS cliente_nome, a.massoterapeuta_id, a.data_hora, a.status, a.criado_em
                FROM agendamento a
                JOIN cliente c ON a.cliente_id = c.id
                ORDER BY a.data_hora DESC
            """)  # SQL com JOIN para buscar agendamentos e nomes dos clientes
            agendamentos = cursor.fetchall()  # Pega todos os resultados
        except DatabaseError as e:  # Se der erro
            print(f"Erro ao buscar agendamentos: {e}")
        finally:  # Sempre executa
            if cursor:  # Se cursor existe
                cursor.close()  # Fecha cursor
            conn.close()  # Fecha conexão
    return agendamentos  # Retorna lista

def listar_agendamentos_massoterapeuta(massoterapeuta_id):
    """
    Retorna agendamentos de um massoterapeuta específico.
    """
    conn = get_connection()  # Conecta ao banco
    agendamentos = []  # Lista vazia
    if conn:  # Se conectou
        cursor = None  # Inicializa cursor
        try:  # Tenta executar
            cursor = conn.cursor(cursor_factory=RealDictCursor)  # Cursor que retorna dict
            cursor.execute("""
                SELECT a.id, a.cliente_id, c.nome AS cliente_nome, c.telefone AS cliente_telefone, 
                       c.email AS cliente_email, a.data_hora, a.sintomas, a.status, a.criado_em
                FROM agendamento a
                JOIN cliente c ON a.cliente_id = c.id
                WHERE a.massoterapeuta_id = %s
                ORDER BY a.data_hora DESC
            """, (massoterapeuta_id,))  # SQL para buscar agendamentos específicos do massoterapeuta
            agendamentos = cursor.fetchall()  # Pega todos os resultados
        except DatabaseError as e:  # Se der erro
            print(f"Erro ao buscar agendamentos do massoterapeuta: {e}")
        finally:  # Sempre executa
            if cursor:  # Se cursor existe
                cursor.close()  # Fecha cursor
            conn.close()  # Fecha conexão
    return agendamentos  # Retorna lista

def atualizar_agendamento(agendamento_id, massoterapeuta_id, novo_status):
    """
    Atualiza o status de um agendamento específico do massoterapeuta.
    Verifica se o agendamento pertence ao massoterapeuta antes de atualizar.
    """
    conn = get_connection()  # Conecta ao banco
    if not conn:  # Se não conectou
        print("Erro: não foi possível conectar ao banco.")
        return False  # Retorna falso

    cursor = None  # Inicializa cursor
    try:  # Tenta executar
        cursor = conn.cursor()  # Cria cursor
        
        # Verifica se o agendamento existe e pertence ao massoterapeuta
        cursor.execute("""
            SELECT id FROM agendamento 
            WHERE id = %s AND massoterapeuta_id = %s
        """, (agendamento_id, massoterapeuta_id))  # SQL para verificar propriedade
        
        if not cursor.fetchone():  # Se não encontrou
            print(f"Agendamento {agendamento_id} não encontrado ou não pertence ao massoterapeuta {massoterapeuta_id}")
            return False  # Retorna falso
        
        # Atualiza o status
        cursor.execute("""
            UPDATE agendamento 
            SET status = %s 
            WHERE id = %s AND massoterapeuta_id = %s
        """, (novo_status, agendamento_id, massoterapeuta_id))  # SQL para atualizar status
        
        conn.commit()  # Confirma alteração
        print(f"Agendamento {agendamento_id} atualizado para status '{novo_status}'")
        return True  # Retorna verdadeiro
        
    except Exception as e:  # Se der erro
        conn.rollback()  # Desfaz alterações
        print(f"Erro ao atualizar agendamento: {e}")
        return False  # Retorna falso
    finally:  # Sempre executa
        if cursor:  # Se cursor existe
            cursor.close()  # Fecha cursor
        conn.close()  # Fecha conexão

def listar_agendamentos_por_status(massoterapeuta_id, status_lista):
    """
    Retorna agendamentos de um massoterapeuta filtrados por lista de status.
    Args:
        massoterapeuta_id: ID do massoterapeuta
        status_lista: Lista de status ['marcado'] ou ['confirmado', 'concluido']
    """
    conn = get_connection()
    agendamentos = []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Cria placeholders para os status (%s, %s, ...)
            placeholders = ', '.join(['%s'] * len(status_lista))
            
            cursor.execute(f"""
                SELECT a.id, a.cliente_id, c.nome AS cliente_nome, c.telefone AS cliente_telefone, 
                       c.email AS cliente_email, c.sexo AS cliente_sexo, a.data_hora, a.sintomas, a.status, a.criado_em
                FROM agendamento a
                JOIN cliente c ON a.cliente_id = c.id
                WHERE a.massoterapeuta_id = %s AND a.status IN ({placeholders})
                ORDER BY a.data_hora DESC
            """, [massoterapeuta_id] + status_lista)
            
            agendamentos = cursor.fetchall()
        except DatabaseError as e:
            print(f"Erro ao buscar agendamentos por status: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return agendamentos

def buscar_paciente_com_historico(massoterapeuta_id, nome_busca):
    """
    Busca paciente por nome e retorna dados completos + histórico de agendamentos.
    Args:
        massoterapeuta_id: ID do massoterapeuta logado
        nome_busca: Nome ou parte do nome do paciente
    Returns:
        Dict com dados do paciente e lista de agendamentos
    """
    conn = get_connection()  # Conecta ao banco
    resultado = {"pacientes": [], "total_encontrados": 0}  # Estrutura de retorno
    
    if conn:  # Se conectou
        cursor = None  # Inicializa cursor
        try:  # Tenta executar
            cursor = conn.cursor(cursor_factory=RealDictCursor)  # Cursor que retorna dict
            
            # Busca pacientes que tenham agendamentos com este massoterapeuta
            cursor.execute("""
                SELECT DISTINCT c.id, c.nome, c.telefone, c.email, c.sexo, c.data_nascimento, c.created_at
                FROM cliente c
                JOIN agendamento a ON c.id = a.cliente_id
                WHERE a.massoterapeuta_id = %s 
                AND LOWER(c.nome) LIKE LOWER(%s)
                ORDER BY c.nome ASC
            """, (massoterapeuta_id, f'%{nome_busca}%'))  # SQL para buscar pacientes por nome
            
            pacientes = cursor.fetchall()  # Pega todos os pacientes
            
            # Para cada paciente, busca o histórico de agendamentos
            for paciente in pacientes:  # Loop pelos pacientes
                cursor.execute("""
                    SELECT a.id, a.data_hora, a.sintomas, a.status, a.criado_em,
                           CASE 
                               WHEN a.data_hora > NOW() THEN 'futuro'
                               ELSE 'passado'
                           END as periodo
                    FROM agendamento a
                    WHERE a.cliente_id = %s AND a.massoterapeuta_id = %s
                    ORDER BY a.data_hora DESC
                """, (paciente['id'], massoterapeuta_id))  # SQL para buscar histórico específico
                
                agendamentos = cursor.fetchall()  # Pega todos os agendamentos do paciente
                
                # Separa agendamentos futuros e passados
                agendamentos_futuros = [a for a in agendamentos if a['periodo'] == 'futuro']  # Lista futuros
                agendamentos_passados = [a for a in agendamentos if a['periodo'] == 'passado']  # Lista passados
                
                paciente_completo = {  # Monta dados completos do paciente
                    "id": paciente["id"],
                    "nome": paciente["nome"],
                    "telefone": paciente["telefone"],
                    "email": paciente["email"],
                    "sexo": paciente["sexo"],
                    "data_nascimento": str(paciente["data_nascimento"]),
                    "cliente_desde": str(paciente["created_at"]),
                    "agendamentos_futuros": agendamentos_futuros,
                    "agendamentos_passados": agendamentos_passados,
                    "total_sessoes": len(agendamentos),
                    "sessoes_futuras": len(agendamentos_futuros),
                    "sessoes_passadas": len(agendamentos_passados)
                }  # Estrutura completa com estatísticas
                
                resultado["pacientes"].append(paciente_completo)  # Adiciona à lista
            
            resultado["total_encontrados"] = len(pacientes)  # Conta total
            
        except DatabaseError as e:  # Se der erro
            print(f"Erro ao buscar paciente: {e}")
        finally:  # Sempre executa
            if cursor:  # Se cursor existe
                cursor.close()  # Fecha cursor
            conn.close()  # Fecha conexão
    
    return resultado  # Retorna dados completos

def cancelar_agendamento_com_motivo(agendamento_id, massoterapeuta_id, motivo):
    """
    Cancela um agendamento com motivo e envia email de notificação para o cliente.
    Args:
        agendamento_id: ID do agendamento a ser cancelado
        massoterapeuta_id: ID do massoterapeuta que está cancelando
        motivo: Motivo do cancelamento fornecido pelo massoterapeuta
    Returns:
        Dict com success/error e dados do agendamento para email
    """
    from .email_api import send_email  # Importa função de email
    
    conn = get_connection()  # Conecta ao banco
    if not conn:  # Se não conectou
        return {"success": False, "erro": "Erro de conexão com banco de dados"}

    cursor = None  # Inicializa cursor
    try:  # Tenta executar
        cursor = conn.cursor(cursor_factory=RealDictCursor)  # Cursor que retorna dict
        
        # Busca dados completos do agendamento antes de cancelar
        cursor.execute("""
            SELECT a.id, a.data_hora, a.status, a.criado_em,
                   c.nome as cliente_nome, c.email as cliente_email, c.telefone as cliente_telefone,
                   m.nome as massoterapeuta_nome, m.telefone as massoterapeuta_telefone
            FROM agendamento a
            JOIN cliente c ON a.cliente_id = c.id
            JOIN massoterapeuta m ON a.massoterapeuta_id = m.id
            WHERE a.id = %s AND a.massoterapeuta_id = %s
        """, (agendamento_id, massoterapeuta_id))  # SQL para buscar dados completos
        
        agendamento = cursor.fetchone()  # Pega o agendamento
        
        if not agendamento:  # Se não encontrou
            return {"success": False, "erro": "Agendamento não encontrado ou você não tem permissão"}
        
        if agendamento['status'] == 'cancelado':  # Se já cancelado
            return {"success": False, "erro": "Este agendamento já foi cancelado"}
        
        if agendamento['status'] == 'concluido':  # Se já concluído
            return {"success": False, "erro": "Não é possível cancelar um agendamento já concluído"}
        
        # Atualiza o status para cancelado
        cursor.execute("""
            UPDATE agendamento 
            SET status = 'cancelado'
            WHERE id = %s AND massoterapeuta_id = %s
        """, (agendamento_id, massoterapeuta_id))  # SQL para cancelar agendamento
        
        # Registra o motivo do cancelamento (opcional: criar tabela para histórico)
        cursor.execute("""
            INSERT INTO agendamento_historico (agendamento_id, acao, motivo, criado_em)
            VALUES (%s, 'cancelamento', %s, NOW())
            ON CONFLICT DO NOTHING
        """, (agendamento_id, motivo))  # SQL para registrar histórico
        
        conn.commit()  # Confirma alterações
        
        # Envia email de notificação para o cliente
        try:  # Tenta enviar email
            data_formatada = agendamento['data_hora'].strftime("%d/%m/%Y às %H:%M")  # Formata data
            assunto = "🚫 Agendamento Cancelado - HM Massoterapia"  # Assunto do email
            
            conteudo = f"""
Olá, {agendamento['cliente_nome']}!

Infelizmente, seu agendamento foi cancelado pelo massoterapeuta.

📅 DADOS DO AGENDAMENTO CANCELADO:
• Data e Hora: {data_formatada}
• Massoterapeuta: {agendamento['massoterapeuta_nome']}
• Telefone do massoterapeuta: {agendamento['massoterapeuta_telefone']}

📝 MOTIVO DO CANCELAMENTO:
{motivo}

Pedimos desculpas pelo inconveniente. Você pode reagendar sua sessão entrando em contato conosco ou pelo nosso sistema.

Para reagendar, acesse: http://localhost:5173

Atenciosamente,
Equipe HM Massoterapia
            """  # Template do email
            
            status_email, resposta_email = send_email(agendamento['cliente_email'], assunto, conteudo)  # Envia email
            
            return {  # Retorna sucesso com detalhes
                "success": True, 
                "mensagem": "Agendamento cancelado com sucesso",
                "agendamento": dict(agendamento),
                "email_enviado": status_email == 202,
                "detalhes_email": resposta_email if status_email != 202 else "Email enviado com sucesso"
            }
            
        except Exception as email_error:  # Se falhar o email
            # Mesmo se o email falhar, o cancelamento foi realizado
            print(f"Erro ao enviar email: {email_error}")
            return {  # Retorna sucesso mesmo com erro de email
                "success": True,
                "mensagem": "Agendamento cancelado com sucesso (erro ao enviar email)",
                "agendamento": dict(agendamento),
                "email_enviado": False,
                "erro_email": str(email_error)
            }
        
    except Exception as e:  # Se der erro geral
        conn.rollback()  # Desfaz alterações
        print(f"Erro ao cancelar agendamento: {e}")
        return {"success": False, "erro": f"Erro interno: {str(e)}"}  # Retorna erro
        
    finally:  # Sempre executa
        if cursor:  # Se cursor existe
            cursor.close()  # Fecha cursor
        conn.close()  # Fecha conexão
