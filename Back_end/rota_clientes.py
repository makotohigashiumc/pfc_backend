# ===== IMPORTS DAS ROTAS DE CLIENTES =====
# Flask: Framework web e funções de requisição/resposta
from flask import Blueprint, request, jsonify
# JWT: Sistema de autenticação - criar e verificar tokens
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
# datetime: Manipulação de datas
from datetime import datetime
# Funções do módulo cliente: Lógica de negócio
from .cliente import (
    cadastrar_cliente,        # Registrar novo cliente
    verificar_login,          # Validar email/senha
    cadastrar_agendamento,    # Criar agendamento (com sintomas)
    atualizar_conta,          # Editar dados do cliente
    excluir_cliente,          # Deletar conta
    historico_sessoes_cliente, # Listar agendamentos
    buscar_cliente_por_id     # Buscar cliente específico
)
# Database e email: Conexão e notificações
from .database import get_connection
from .email_api import send_email, generate_confirmation_token, verify_confirmation_token
import os
from werkzeug.security import generate_password_hash

# ===== CRIAÇÃO DO BLUEPRINT =====
# Blueprint: Organiza as rotas em grupos (todas as rotas de cliente ficam aqui)
rota_clientes = Blueprint('rota_clientes', __name__)

# ================================================================
# ENDPOINT: CONFIRMAÇÃO DE EMAIL
# URL: POST /api/clientes/confirmar-email/<token>
# ================================================================
@rota_clientes.route('/api/clientes/confirmar-email/<token>', methods=['POST'])
def confirmar_email(token):
    """
    PROPÓSITO: Ativa a conta do cliente após verificar email
    
    FLUXO:
    1. Cliente recebe email com link/token
    2. Cliente clica no link
    3. Sistema valida token
    4. Marca email como confirmado
    5. Cliente pode fazer login
    
    PARÂMETROS:
    - token: Código único enviado por email
    
    RETORNA:
    - Sucesso: {"mensagem": "Email confirmado"}
    - Erro: {"erro": "Token inválido"}
    """
    from .email_api import verify_confirmation_token
    from . import database
    import traceback
    try:
        # ===== VALIDAÇÃO DO TOKEN =====
        # Verifica se token é válido e não expirou
        email = verify_confirmation_token(token)
        if not email:
            print(f"[CONFIRMAÇÃO] Token inválido ou expirado: {token}")
            return {"erro": "Token inválido ou expirado."}, 400
        # Atualiza email_confirmado no banco
        conn = database.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE cliente SET email_confirmado=TRUE WHERE email=%s", (email,))
        conn.commit()
        cur.close()
        conn.close()
        print(f"[CONFIRMAÇÃO] E-mail confirmado: {email}")
        return {"mensagem": "E-mail confirmado com sucesso!"}, 200
    except Exception as e:
        print(f"[CONFIRMAÇÃO] Erro ao confirmar: {str(e)}\n{traceback.format_exc()}")
        return {"erro": f"Erro ao confirmar e-mail: {str(e)}"}, 400

# -------------------------------
# ROTA: Solicitar recuperação de senha
@rota_clientes.route('/api/clientes/recuperar-senha', methods=['POST'])
def recuperar_senha():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"erro": "Email é obrigatório."}), 400
    # Gera token de redefinição
    token = generate_confirmation_token(email)
    reset_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')}/redefinir-senha?token={token}"
    subject = "Recuperação de senha - Massoterapia TCC"
    content = f"Olá! Para redefinir sua senha, clique no link: {reset_url}\nEste link expira em 24 horas."
    status, resp = send_email(email, subject, content)
    if status == 202:
        return jsonify({"mensagem": "Email de recuperação enviado."})
    else:
        return jsonify({"erro": "Falha ao enviar email."}), 500

# -------------------------------
# ROTA: Redefinir senha
@rota_clientes.route('/api/clientes/redefinir-senha', methods=['POST'])
def redefinir_senha():
    data = request.get_json()
    token = data.get('token')
    nova_senha = data.get('nova_senha')
    if not token or not nova_senha:
        return jsonify({"erro": "Token e nova senha são obrigatórios."}), 400
    email = verify_confirmation_token(token)
    if not email:
        return jsonify({"erro": "Token inválido ou expirado."}), 400
    # Atualiza senha no banco
    conn = get_connection()
    cur = conn.cursor()
    hashed = generate_password_hash(nova_senha)
    cur.execute("UPDATE cliente SET senha_hash=%s WHERE email=%s", (hashed, email))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": "Senha redefinida com sucesso."})
# ================================================================
# ENDPOINT: CADASTRO DE CLIENTE
# URL: POST /api/clientes
# ================================================================
@rota_clientes.route('/api/clientes', methods=['POST'])
def api_cadastrar_cliente():
    """
    PROPÓSITO: Registra um novo cliente no sistema
    
    DADOS OBRIGATÓRIOS (JSON):
    - nome: Nome completo
    - telefone: Número de contato
    - sexo: "Masculino" ou "Feminino"
    - data_nascimento: "YYYY-MM-DD"
    - email: Email único
    - senha: Senha (será criptografada)
    
    FLUXO:
    1. Valida campos obrigatórios
    2. Chama função cadastrar_cliente()
    3. Envia email de confirmação
    4. Retorna sucesso/erro
    """
    # ===== OBTENÇÃO DOS DADOS =====
    data = request.get_json()
    
    # ===== VALIDAÇÃO DOS CAMPOS OBRIGATÓRIOS =====
    if not data or not all(k in data for k in ("nome", "telefone", "sexo", "data_nascimento", "email", "senha")):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400
    
    # ===== CHAMADA DA FUNÇÃO DE CADASTRO =====
    resultado = cadastrar_cliente(
        data['nome'], data['telefone'], data['sexo'],
        data['data_nascimento'], data['email'], data['senha']
    )
    
    # ===== TRATAMENTO DE ERROS =====
    if isinstance(resultado, dict) and "erro" in resultado:
        return jsonify({"erro": resultado["erro"]}), 400
    if not resultado:
        return jsonify({"erro": "Falha ao cadastrar cliente"}), 400
    
    # ===== RETORNO DE SUCESSO =====
    return jsonify({"mensagem": "Cadastro realizado! Confirme seu e-mail para acessar o sistema.", "id": resultado}), 201

# ================================================================
# ENDPOINT: LOGIN DO CLIENTE
# URL: POST /api/clientes/login
# ================================================================
@rota_clientes.route('/api/clientes/login', methods=['POST'])
def api_login():
    """
    PROPÓSITO: Autentica cliente e gera token JWT
    
    DADOS OBRIGATÓRIOS (JSON):
    - email: Email do cliente
    - senha: Senha do cliente
    
    RETORNA:
    - Sucesso: Token JWT + dados do usuário
    - Erro: Mensagem de erro 401
    """
    # ===== OBTENÇÃO DOS DADOS =====
    data = request.get_json()
    
    # ===== VALIDAÇÃO DOS CAMPOS =====
    if not data or not all(k in data for k in ("email", "senha")):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400
    
    # ===== VERIFICAÇÃO DE LOGIN =====
    usuario = verificar_login(data['email'], data['senha'])
    if usuario:
        # ===== GERAÇÃO DE TOKEN JWT =====
        # Token é usado para autenticar requisições futuras
        token = create_access_token(identity=str(usuario['id']))
        return jsonify({
            "mensagem": "Login realizado com sucesso",
            "usuario": usuario,
            "token": token
        })
    
    # ===== ERRO DE AUTENTICAÇÃO =====
    return jsonify({"erro": "Email, senha inválidos ou e-mail não confirmado."}), 401

# ================================================================
# ENDPOINT: CRIAR AGENDAMENTO (COM SINTOMAS) - FUNCIONALIDADE PRINCIPAL
# URL: POST /api/clientes/agendamentos
# ================================================================
@rota_clientes.route('/api/clientes/agendamentos', methods=['POST'])
@jwt_required()  # 🔒 PROTEÇÃO: Só clientes logados podem agendar
def api_cadastrar_agendamento():
    """
    PROPÓSITO: Cria novo agendamento com descrição de sintomas
    
    ⭐ ESTA É A FUNCIONALIDADE PRINCIPAL QUE IMPLEMENTAMOS ⭐
    
    DADOS OBRIGATÓRIOS (JSON):
    - massoterapeuta_id: ID do profissional escolhido
    - data_hora: "YYYY-MM-DDTHH:MM" (formato ISO)
    
    DADOS OPCIONAIS (JSON):
    - sintomas: Descrição dos sintomas do cliente (NOVO CAMPO)
    
    AUTENTICAÇÃO:
    - Requer token JWT no header Authorization
    - Sistema identifica automaticamente o cliente logado
    
    VALIDAÇÕES AUTOMÁTICAS:
    - Horário de funcionamento (8:30-18:30)
    - Dias úteis (segunda a quinta)
    - Conflitos de horário
    - Agendamentos passados
    
    RETORNA:
    - Sucesso: Dados do agendamento criado
    - Erro: Mensagem específica do problema
    """
    # ===== IDENTIFICAÇÃO DO CLIENTE =====
    # get_jwt_identity() extrai o ID do cliente do token JWT
    user_id = get_jwt_identity()
    
    # ===== OBTENÇÃO DOS DADOS =====
    data = request.get_json()
    
    # ===== VALIDAÇÃO DOS CAMPOS OBRIGATÓRIOS =====
    if not data or not all(k in data for k in ("massoterapeuta_id", "data_hora")):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400
    
    # ===== EXTRAÇÃO DOS SINTOMAS (NOVA FUNCIONALIDADE) =====
    # Campo opcional - se não informado, fica como None
    sintomas = data.get('sintomas', None)
    
    # ===== CRIAÇÃO DO AGENDAMENTO =====
    # Passa TODOS os parâmetros incluindo sintomas
    agendamento = cadastrar_agendamento(user_id, data['massoterapeuta_id'], data['data_hora'], sintomas)
    
    # ===== TRATAMENTO DE ERRO =====
    if not agendamento:
        return jsonify({"erro": "Falha ao criar agendamento"}), 400
    
    # ===== RETORNO DE SUCESSO =====
    return jsonify({"mensagem": "Agendamento cadastrado com sucesso", "agendamento": agendamento}), 201

# -------------------------------
# ROTA: Histórico de agendamentos do cliente
# -------------------------------
@rota_clientes.route('/api/clientes/agendamentos', methods=['GET'])
@jwt_required()
def api_historico_agendamentos():
    try:
        user_id = get_jwt_identity()
        incluir_futuros = request.args.get("incluir_futuros", "true").lower() == "true"
        historico = historico_sessoes_cliente(user_id, incluir_futuros=incluir_futuros)
        # Garante que data_hora seja string formatada
        for h in historico:
            if isinstance(h.get('data_hora'), (str, type(None))):
                continue
            h['data_hora'] = h['data_hora'].strftime('%Y-%m-%d %H:%M')
        return jsonify(historico or [])
    except Exception as e:
        print(f"Erro ao buscar histórico de agendamentos: {e}")
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 422

# -------------------------------
# ROTA: Atualizar cliente
# -------------------------------
@rota_clientes.route('/api/clientes', methods=['PUT'])
@jwt_required()
def api_atualizar_cliente():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or not all(k in data for k in ("nome", "telefone", "email")):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400
    atualizar_conta(user_id, data['nome'], data['telefone'], data['email'])
    return jsonify({"mensagem": "Cliente atualizado com sucesso"})

# -------------------------------
# ROTA: Excluir cliente
# -------------------------------
@rota_clientes.route('/api/clientes', methods=['DELETE'])
@jwt_required()
def api_excluir_cliente():
    user_id = get_jwt_identity()
    excluir_cliente(user_id)
    return jsonify({"mensagem": "Cliente excluído com sucesso"})

# -------------------------------
# ROTA: Buscar cliente por ID (dados do próprio cliente)
# -------------------------------
@rota_clientes.route('/api/clientes/me', methods=['GET'])
@jwt_required()
def api_me():
    user_id = get_jwt_identity()
    usuario = buscar_cliente_por_id(user_id)
    if not usuario:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify(usuario)

# -------------------------------
# ROTA: Horários ocupados do massoterapeuta
# -------------------------------
@rota_clientes.route('/api/massoterapeuta/horarios_ocupados/<int:massoterapeuta_id>', methods=['GET'])
@jwt_required()
def horarios_ocupados_massoterapeuta(massoterapeuta_id):
    from .database import get_connection
    conn = get_connection()
    horarios = []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            # Busca todos os horários ocupados do massoterapeuta, independente do cliente
            cursor.execute("""
                SELECT data_hora FROM agendamento
                WHERE massoterapeuta_id = %s AND status IN ('marcado', 'confirmado', 'pendente')
            """, (massoterapeuta_id,))
            rows = cursor.fetchall()
            horarios = [{"data_hora": row[0].strftime("%Y-%m-%d %H:%M:%S")} for row in rows]
        except Exception as e:
            print(f"Erro ao buscar horários ocupados: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return jsonify(horarios)

# -------------------------------
# ROTA: Cancelar agendamento do cliente
# -------------------------------
@rota_clientes.route('/api/clientes/agendamentos/<int:agendamento_id>/cancelar', methods=['POST'])
@jwt_required()
def cancelar_agendamento_cliente(agendamento_id):
    try:
        user_id = get_jwt_identity()
        conn = get_connection()
        if not conn:
            return jsonify({"erro": "Erro de conexão com o banco"}), 500
        cursor = conn.cursor()
        # Verifica se o agendamento pertence ao cliente logado e pode ser cancelado
        cursor.execute("SELECT id FROM agendamento WHERE id = %s AND cliente_id = %s AND status IN ('marcado', 'pendente')", (agendamento_id, user_id))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"erro": "Agendamento não encontrado ou não pode ser cancelado"}), 404
        # Atualiza status para cancelado
        cursor.execute("UPDATE agendamento SET status = 'cancelado' WHERE id = %s", (agendamento_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Agendamento cancelado com sucesso"})
    except Exception as e:
        print(f"Erro ao cancelar agendamento: {e}")
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

# -------------------------------
# ROTA: Limpar histórico de agendamentos do cliente
# -------------------------------
@rota_clientes.route('/api/clientes/agendamentos/limpar', methods=['POST'])
@jwt_required()
def limpar_historico_agendamentos():
    try:
        user_id = get_jwt_identity()
        conn = get_connection()
        if not conn:
            return jsonify({"erro": "Erro de conexão com o banco"}), 500
        cursor = conn.cursor()
        # Exclui todos os agendamentos do cliente
        cursor.execute("DELETE FROM agendamento WHERE cliente_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Histórico de agendamentos limpo com sucesso"})
    except Exception as e:
        print(f"Erro ao limpar histórico de agendamentos: {e}")
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500