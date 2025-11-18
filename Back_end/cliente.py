from Back_end.database import get_connection
from psycopg2 import DatabaseError, errors
from psycopg2.extras import RealDictCursor
from datetime import datetime, time
from werkzeug.security import generate_password_hash, check_password_hash

# ================================================================
# FUNÇÃO PRINCIPAL: CADASTRAR NOVO CLIENTE
# ================================================================
def cadastrar_cliente(nome, telefone, sexo, data_nascimento, email, senha):
    """
    PROPÓSITO: Registra um novo cliente no sistema
    
    ETAPAS:
    1. Valida dados de entrada
    2. Verifica se email/telefone já existem
    3. Criptografa a senha
    4. Insere no banco de dados
    5. Envia email de confirmação
    
    PARÂMETROS:
    - nome: Nome completo do cliente
    - telefone: Número de contato
    - sexo: "Masculino" ou "Feminino"
    - data_nascimento: Data no formato "YYYY-MM-DD"
    - email: Email único do cliente
    - senha: Senha em texto puro (será criptografada)
    
    RETORNA:
    - Sucesso: ID do cliente criado
    - Erro: Dicionário com mensagem de erro
    """
    
    print(f"Tentando inserir cliente: nome={nome}, telefone={telefone}, sexo={sexo}, data_nascimento={data_nascimento}, email={email}")
    
    if not data_nascimento or sexo not in ["Masculino", "Feminino"]:
        print(f"Erro: sexo ou data_nascimento inválido")
        return None
    
    try:
        data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    except ValueError:
        print(f"Erro: data_nascimento '{data_nascimento}' inválida")
        return None
    
    conn = get_connection()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM cliente WHERE email = %s", (email,))
            if cursor.fetchone():
                print(f"Erro: Email '{email}' já cadastrado")
                return {"erro": "Já existe uma conta com este e-mail."}
            
            cursor.execute("SELECT id FROM cliente WHERE telefone = %s", (telefone,))
            if cursor.fetchone():
                print(f"Erro: Telefone '{telefone}' já cadastrado")
                return {"erro": "Já existe uma conta com este número de telefone."}
            
            senha_hash = generate_password_hash(senha)
            
            sql = """
                INSERT INTO cliente (nome, telefone, sexo, data_nascimento, email, senha_hash, email_confirmado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """
            cursor.execute(sql, (nome, telefone, sexo, data_nascimento, email, senha_hash, False))
            
            cliente_id = cursor.fetchone()[0]
            
            conn.commit()
            print(f"Cliente inserido com sucesso! ID: {cliente_id}")
            
            try:
                from Back_end.email_api import send_confirmation_email
                status, resp = send_confirmation_email(email)
                print(f"Status envio e-mail: {status}, resposta: {resp}")
            except Exception as e:
                print(f"Erro ao enviar e-mail de confirmação: {e}")
            return cliente_id
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir cliente: {e}")
            return {"erro": "Falha ao cadastrar cliente."}
        finally:
            if cursor:
                cursor.close()
            conn.close()

def verificar_login(email, senha):
    conn = get_connection()
    usuario = None
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM cliente WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if usuario and check_password_hash(usuario['senha_hash'], senha):
                if not usuario.get('email_confirmado', False):
                    print("Email não confirmado. Bloqueando login.")
                    return None
                usuario.pop('senha_hash')
                return usuario
            return None
        except Exception as e:
            print(f"Erro ao verificar login: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

# ================================================================
# FUNÇÃO CRÍTICA: CADASTRAR AGENDAMENTO (COM SINTOMAS)
# ================================================================
def cadastrar_agendamento(cliente_id, massoterapeuta_id, data_hora, sintomas=None, status='pendente'):
    """
    PROPÓSITO: Cria um novo agendamento no sistema
    
    FUNCIONALIDADES:
    1. Valida data/horário
    2. Verifica dias de funcionamento (seg-qui)
    3. Impede agendamentos passados
    4. Salva sintomas do cliente (NOVA FUNCIONALIDADE)
    5. Insere no banco com status 'pendente'
    
    PARÂMETROS:
    - cliente_id: ID do cliente que está agendando
    - massoterapeuta_id: ID do massoterapeuta escolhido
    - data_hora: Data e hora desejadas (string ou datetime)
    - sintomas: Descrição dos sintomas (OPCIONAL - novo campo)
    - status: Status inicial ('pendente' por padrão)
    
    RETORNA:
    - Sucesso: Dados completos do agendamento
    - Erro: None
    """
    
    print(f"Tentando inserir agendamento: cliente_id={cliente_id}, massoterapeuta_id={massoterapeuta_id}, data_hora={data_hora}, sintomas={sintomas}, status={status}")
    
    import pytz
    if isinstance(data_hora, str):
        try:
            # Formato vindo do frontend: "YYYY-MM-DDTHH:MM"
            if 'T' in data_hora:
                data_hora = datetime.strptime(data_hora, "%Y-%m-%dT%H:%M")
            else:
                # Formatos alternativos com espaço
                try:
                    data_hora = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    data_hora = datetime.strptime(data_hora, "%Y-%m-%d %H:%M")
            # Assume que o horário recebido é no fuso do Brasil (America/Sao_Paulo)
            tz_br = pytz.timezone('America/Sao_Paulo')
            data_hora = tz_br.localize(data_hora)
        except ValueError as e:
            print(f"Erro ao converter data_hora: {e}")
            return None

    tz_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(tz_br)
    if data_hora < agora:
        print("Erro: Não é possível agendar para horários passados.")
        return None

    dia_semana = data_hora.weekday()
    if dia_semana < 0 or dia_semana > 3:  # 0-3 = segunda a quinta
        print("Erro: Agendamentos só podem ser feitos de segunda a quinta-feira")
        return {"erro": "Agendamentos só podem ser feitos de segunda a quinta-feira"}

    hora_inicio = time(8, 0)
    hora_fim = time(18, 0)
    if not (hora_inicio <= data_hora.time() <= hora_fim):
        print("Erro: Horário fora do funcionamento da clínica (8:00 às 18:00)")
        return None

    conn = get_connection()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM agendamento
                WHERE massoterapeuta_id = %s AND data_hora = %s AND status IN ('marcado', 'confirmado', 'pendente')
            """, (massoterapeuta_id, data_hora))
            masso_conf = cursor.fetchone()
            if masso_conf:
                print(f"Erro: Massoterapeuta já tem agendamento neste horário")
                return {"erro": "Massoterapeuta já tem agendamento neste horário", "agendamento": masso_conf}

            cursor.execute("""
                SELECT * FROM agendamento
                WHERE cliente_id = %s AND data_hora = %s AND status IN ('marcado', 'confirmado', 'pendente')
            """, (cliente_id, data_hora))
            cliente_conf = cursor.fetchone()
            if cliente_conf:
                print(f"Erro: Cliente já tem agendamento neste horário")
                return {"erro": "Cliente já tem agendamento neste horário", "agendamento": cliente_conf}

            sql = """
                INSERT INTO agendamento (cliente_id, massoterapeuta_id, data_hora, sintomas, status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, cliente_id, massoterapeuta_id, data_hora, sintomas, status;
            """
            cursor.execute(sql, (cliente_id, massoterapeuta_id, data_hora, sintomas, status))
            agendamento = cursor.fetchone()
            
            conn.commit()
            print(f"Agendamento inserido com sucesso: {agendamento}")
            
            try:
                cursor.execute("SELECT email, nome, telefone FROM cliente WHERE id = %s", (cliente_id,))
                cliente = cursor.fetchone()
                
                if cliente:
                    destinatario = cliente[0]  # email
                    nome_cliente = cliente[1]  # nome
                    telefone_cliente = cliente[2]  # telefone
                    
                    try:
                        from Back_end.email_api import sendgrid_email_api_massoterapia
                        assunto = "Solicitação de Agendamento Recebida"
                        conteudo = f"Olá {nome_cliente}, sua solicitação de agendamento para {data_hora} foi recebida e está aguardando confirmação da clínica. Você será notificado quando o agendamento for confirmado."
                        status, resp = sendgrid_email_api_massoterapia(destinatario, assunto, conteudo)
                        print(f"Status envio e-mail agendamento: {status}, resposta: {resp}")
                    except Exception as e:
                        print(f"Erro ao enviar e-mail de agendamento: {e}")
                    
                    # Caso queira reativar notificações via outro canal, implemente aqui.
                        
            except Exception as e:
                print(f"Erro ao enviar notificações de agendamento: {e}")
            return agendamento
        except Exception as e:
            conn.rollback()
            print(f"Erro ao inserir agendamento: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

def atualizar_conta(id, nome, telefone, email):
    conn = get_connection()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cliente WHERE email = %s AND id != %s", (email, id))
            if cursor.fetchone():
                print(f"Erro: email '{email}' já cadastrado por outro cliente")
                return
            sql = "UPDATE cliente SET nome = %s, telefone = %s, email = %s WHERE id = %s"
            cursor.execute(sql, (nome, telefone, email, id))
            conn.commit()
            print(f"Cliente {id} atualizado com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao atualizar cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

def excluir_cliente(id):
    conn = get_connection()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM cliente WHERE id = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            print(f"Cliente {id} excluído com sucesso!")
        except Exception as e:
            conn.rollback()
            print(f"Erro ao excluir cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()

def historico_sessoes_cliente(cliente_id, incluir_futuros=True):
    conn = get_connection()
    historico = []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            sql = """
                SELECT a.id, a.data_hora, a.sintomas, a.status, a.criado_em, m.nome AS massoterapeuta_nome
                FROM agendamento a
                JOIN massoterapeuta m ON a.massoterapeuta_id = m.id
                WHERE a.cliente_id = %s
            """
            if not incluir_futuros:
                sql += " AND status IN ('realizado', 'cancelado')"
            sql += " ORDER BY data_hora DESC"
            cursor.execute(sql, (cliente_id,))
            historico = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar histórico de sessões do cliente: {e}")
            raise Exception(f"Erro ao buscar histórico de sessões do cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return historico

def buscar_cliente_por_id(cliente_id):
    conn = get_connection()
    cliente = None
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            sql = "SELECT id, nome, telefone, email, created_at FROM cliente WHERE id = %s"
            cursor.execute(sql, (cliente_id,))
            cliente = cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar cliente por id: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()