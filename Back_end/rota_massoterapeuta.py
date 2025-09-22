from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .massoterapeuta import listar_agendamentos, listar_massoterapeutas, listar_clientes, listar_agendamentos_massoterapeuta, verificar_login
from flask_jwt_extended import create_access_token
# -------------------------------
# Login do massoterapeuta
# -------------------------------
rota_massoterapeuta = Blueprint('rota_massoterapeuta', __name__)

@rota_massoterapeuta.route('/api/massoterapeuta/login', methods=['POST'])
def login_massoterapeuta():
    data = request.get_json()
    usuario = verificar_login(data['email'], data['senha'])
    if usuario:
        token = create_access_token(identity=str(usuario['id']))
        return jsonify({"mensagem": "Login realizado com sucesso", "usuario": usuario, "token": token})
    else:
        return jsonify({"erro": "Email, senha inválidos ou e-mail não confirmado"}), 401

# -------------------------------
# Blueprint de rotas para massoterapeuta
# -------------------------------

# -------------------------------
# Listar todos os massoterapeutas (opcional para dropdown de seleção de clientes)
# -------------------------------
@rota_massoterapeuta.route('/api/massoterapeuta/lista', methods=['GET'])
def get_massoterapeutas():
    """
    Retorna lista de massoterapeutas (id, nome, telefone, email).
    Pode ser usado para dropdown na criação de agendamentos.
    """
    try:
        massoterapeutas = listar_massoterapeutas()
        lista = [
            {
                "id": m["id"],
                "nome": m["nome"],
                "telefone": m["telefone"],
                "email": m["email"]
            } for m in massoterapeutas
        ]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar massoterapeutas: {str(e)}"}), 500

# -------------------------------
# Listar todos os clientes (informações visíveis para massoterapeuta)
# -------------------------------
@rota_massoterapeuta.route('/api/massoterapeuta/clientes', methods=['GET'])
@jwt_required()
def get_clientes():
    """
    Retorna informações básicas dos clientes (id, nome, telefone, email, criado_em).
    Massoterapeuta precisa estar logado para acessar.
    """
    try:
        clientes = listar_clientes()
        return jsonify(clientes)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar clientes: {str(e)}"}), 500

# -------------------------------
# Listar todos os agendamentos do massoterapeuta logado
# -------------------------------
@rota_massoterapeuta.route('/api/massoterapeuta/agendamentos', methods=['GET'])
@jwt_required()
def get_agendamentos():
    """
    Retorna agendamentos específicos do massoterapeuta logado.
    Inclui cliente_id, cliente_nome, data_hora, status e criado_em.
    """
    massoterapeuta_id = get_jwt_identity()
    try:
        agendamentos = listar_agendamentos_massoterapeuta(massoterapeuta_id)
        lista = [
            {
                "id": a["id"],
                "cliente_id": a["cliente_id"],
                "cliente_nome": a["cliente_nome"],
                "data_hora": str(a["data_hora"]),
                "status": a["status"],
                "criado_em": str(a["criado_em"])
            } for a in agendamentos
        ]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar agendamentos: {str(e)}"}), 500
