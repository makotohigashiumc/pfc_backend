from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import datetime
from .cliente import (
    cadastrar_cliente,
    verificar_login,
    cadastrar_agendamento,
    atualizar_conta,
    excluir_cliente,
    historico_sessoes_cliente,
    buscar_cliente_por_id
)
from Back_end.database import get_connection

rota_clientes = Blueprint('rota_clientes', __name__)

# -------------------------------
# ROTA: Cadastrar cliente
# -------------------------------
@rota_clientes.route('/api/clientes', methods=['POST'])
def api_cadastrar_cliente():
    data = request.get_json()
    if not data or not all(k in data for k in ("nome", "telefone", "sexo", "data_nascimento", "email", "senha")):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400
    cliente_id = cadastrar_cliente(
        data['nome'], data['telefone'], data['sexo'],
        data['data_nascimento'], data['email'], data['senha']
    )
    if not cliente_id:
        return jsonify({"erro": "Falha ao cadastrar cliente"}), 400
    return jsonify({"mensagem": "Cliente cadastrado com sucesso", "id": cliente_id}), 201

# -------------------------------
# ROTA: Login do cliente
# -------------------------------
@rota_clientes.route('/api/clientes/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "senha")):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400
    usuario = verificar_login(data['email'], data['senha'])
    if usuario:
        token = create_access_token(identity=str(usuario['id']))
        return jsonify({
            "mensagem": "Login realizado com sucesso",
            "usuario": usuario,
            "token": token
        })
    return jsonify({"erro": "Email ou senha inválidos"}), 401

# -------------------------------
# ROTA: Criar agendamento
# -------------------------------
@rota_clientes.route('/api/clientes/agendamentos', methods=['POST'])
@jwt_required()
def api_cadastrar_agendamento():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or not all(k in data for k in ("massoterapeuta_id", "data_hora")):
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400
    agendamento = cadastrar_agendamento(user_id, data['massoterapeuta_id'], data['data_hora'])
    if not agendamento:
        return jsonify({"erro": "Falha ao criar agendamento"}), 400
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
            cursor.execute("""
                SELECT data_hora FROM agendamento
                WHERE massoterapeuta_id = %s AND status = 'marcado'
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
        # Verifica se o agendamento pertence ao cliente logado e está marcado
        cursor.execute("SELECT id FROM agendamento WHERE id = %s AND cliente_id = %s AND status = 'marcado'", (agendamento_id, user_id))
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