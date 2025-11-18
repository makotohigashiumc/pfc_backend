from Back_end.database import get_connection
from psycopg2 import OperationalError, DatabaseError, errors
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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
                SELECT a.id, a.cliente_id, c.nome AS cliente_nome, c.telefone AS cliente_telefone, 
                       c.email AS cliente_email, a.data_hora, a.sintomas, a.status, a.criado_em
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

def atualizar_agendamento(agendamento_id, massoterapeuta_id, novo_status):
    """
    Atualiza o status de um agendamento específico do massoterapeuta.
    Verifica se o agendamento pertence ao massoterapeuta antes de atualizar.
    """
    conn = get_connection()
    if not conn:
        print("Erro: não foi possível conectar ao banco.")
        return False

    cursor = None
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM agendamento WHERE id = %s AND massoterapeuta_id = %s",
            (agendamento_id, massoterapeuta_id)
        )

        if not cursor.fetchone():
            print(f"Agendamento {agendamento_id} não encontrado ou não pertence ao massoterapeuta {massoterapeuta_id}")
            return False

        cursor.execute(
            """
            SELECT a.data_hora, c.nome, c.telefone, c.email, m.nome as massoterapeuta_nome
            FROM agendamento a
            JOIN cliente c ON a.cliente_id = c.id
            JOIN massoterapeuta m ON a.massoterapeuta_id = m.id
            WHERE a.id = %s AND a.massoterapeuta_id = %s
            """,
            (agendamento_id, massoterapeuta_id),
        )

        dados_agendamento = cursor.fetchone()
        if not dados_agendamento:
            print("Erro: dados do agendamento não encontrados")
            return False

        data_hora = dados_agendamento[0]
        nome_cliente = dados_agendamento[1]
        telefone_cliente = dados_agendamento[2]
        email_cliente = dados_agendamento[3]
        massoterapeuta_nome = dados_agendamento[4]

        cursor.execute(
            "UPDATE agendamento SET status = %s WHERE id = %s AND massoterapeuta_id = %s",
            (novo_status, agendamento_id, massoterapeuta_id),
        )

        conn.commit()
        print(f"Agendamento {agendamento_id} atualizado para status '{novo_status}'")

        try:
            if isinstance(data_hora, str):
                from datetime import datetime as _dt
                try:
                    data_dt = _dt.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    data_dt = data_hora
            else:
                data_dt = data_hora

            try:
                data_formatada = data_dt.strftime("%d/%m/%Y às %H:%M") if hasattr(data_dt, 'strftime') else str(data_dt)
            except Exception:
                data_formatada = str(data_dt)

            print(f"LOG: notificação whatsapp desabilitada - agendamento={agendamento_id}, status={novo_status}, data_hora={data_formatada}, telefone={telefone_cliente}")
        except Exception:
            pass

        return True
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print(f"Erro ao atualizar agendamento: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conn.close()
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
    conn = get_connection()
    resultado = {"pacientes": [], "total_encontrados": 0}
    
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT DISTINCT c.id, c.nome, c.telefone, c.email, c.sexo, c.data_nascimento, c.created_at
                FROM cliente c
                JOIN agendamento a ON c.id = a.cliente_id
                WHERE a.massoterapeuta_id = %s 
                AND LOWER(c.nome) LIKE LOWER(%s)
                ORDER BY c.nome ASC
            """, (massoterapeuta_id, f'%{nome_busca}%'))
            
            pacientes = cursor.fetchall()
            
            for paciente in pacientes:
                cursor.execute("""
                    SELECT a.id, a.data_hora, a.sintomas, a.status, a.criado_em,
                           CASE 
                               WHEN a.data_hora > NOW() THEN 'futuro'
                               ELSE 'passado'
                           END as periodo
                    FROM agendamento a
                    WHERE a.cliente_id = %s AND a.massoterapeuta_id = %s
                    ORDER BY a.data_hora DESC
                """, (paciente['id'], massoterapeuta_id))
                
                agendamentos = cursor.fetchall()
                
                agendamentos_futuros = [a for a in agendamentos if a['periodo'] == 'futuro']
                agendamentos_passados = [a for a in agendamentos if a['periodo'] == 'passado']
                
                paciente_completo = {
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
                }
                
                resultado["pacientes"].append(paciente_completo)
            
            resultado["total_encontrados"] = len(pacientes)
            
        except DatabaseError as e:
            print(f"Erro ao buscar paciente: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    return resultado

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
    from Back_end.email_api import send_email
    
    conn = get_connection()
    if not conn:
        return {"success": False, "erro": "Erro de conexão com banco de dados"}

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT a.id, a.data_hora, a.status, a.criado_em,
                   c.nome as cliente_nome, c.email as cliente_email, c.telefone as cliente_telefone,
                   m.nome as massoterapeuta_nome, m.telefone as massoterapeuta_telefone
            FROM agendamento a
            JOIN cliente c ON a.cliente_id = c.id
            JOIN massoterapeuta m ON a.massoterapeuta_id = m.id
            WHERE a.id = %s AND a.massoterapeuta_id = %s
        """, (agendamento_id, massoterapeuta_id))
        
        agendamento = cursor.fetchone()
        
        if not agendamento:
            return {"success": False, "erro": "Agendamento não encontrado ou você não tem permissão"}
        
        if agendamento['status'] == 'cancelado':
            return {"success": False, "erro": "Este agendamento já foi cancelado"}
        
        if agendamento['status'] == 'concluido':
            return {"success": False, "erro": "Não é possível cancelar um agendamento já concluído"}
        
        cursor.execute("""
            UPDATE agendamento 
            SET status = 'cancelado'
            WHERE id = %s AND massoterapeuta_id = %s
        """, (agendamento_id, massoterapeuta_id))
        
        cursor.execute("""
            INSERT INTO agendamento_historico (agendamento_id, acao, motivo, criado_em)
            VALUES (%s, 'cancelamento', %s, NOW())
            ON CONFLICT DO NOTHING
        """, (agendamento_id, motivo))
        
        conn.commit()
        
        try:
            data_formatada = agendamento['data_hora'].strftime("%d/%m/%Y às %H:%M")
            assunto = "🚫 Agendamento Cancelado - HM Massoterapia"
            
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
            """
            
            status_email, resposta_email = send_email(agendamento['cliente_email'], assunto, conteudo)
            
            return {
                "success": True, 
                "mensagem": "Agendamento cancelado com sucesso",
                "agendamento": dict(agendamento),
                "email_enviado": status_email == 202,
                "detalhes_email": resposta_email if status_email != 202 else "Email enviado com sucesso"
            }
            
        except Exception as email_error:
            print(f"Erro ao enviar email: {email_error}")
            return {
                "success": True,
                "mensagem": "Agendamento cancelado com sucesso (erro ao enviar email)",
                "agendamento": dict(agendamento),
                "email_enviado": False,
                "erro_email": str(email_error)
            }
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cancelar agendamento: {e}")
        return {"success": False, "erro": f"Erro interno: {str(e)}"}
        
    finally:
        if cursor:
            cursor.close()
        conn.close()
