from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Back_end.massoterapeuta import listar_agendamentos, listar_massoterapeutas, listar_clientes, listar_agendamentos_massoterapeuta, verificar_login, atualizar_conta, atualizar_agendamento, listar_agendamentos_por_status, buscar_paciente_com_historico, cancelar_agendamento_com_motivo
from Back_end.cliente import excluir_cliente
from flask_jwt_extended import create_access_token

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

@rota_massoterapeuta.route('/api/massoterapeuta/agendamentos/pendentes', methods=['GET'])
@jwt_required()
def get_agendamentos_pendentes():
    """
    Retorna agendamentos com status 'pendente' e 'marcado' do massoterapeuta logado.
    Para serem confirmados ou cancelados.
    """
    massoterapeuta_id = get_jwt_identity()
    try:
        agendamentos = listar_agendamentos_por_status(massoterapeuta_id, ['pendente', 'marcado'])
        lista = [
            {
                "id": a["id"],
                "cliente_id": a["cliente_id"],
                "cliente_nome": a["cliente_nome"],
                "cliente_telefone": a.get("cliente_telefone", ""),
                "cliente_email": a.get("cliente_email", ""),
                "data_hora": str(a["data_hora"]),
                "sintomas": a.get("sintomas"),
                "status": a["status"],
                "criado_em": str(a["criado_em"])
            } for a in agendamentos
        ]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar agendamentos pendentes: {str(e)}"}), 500

@rota_massoterapeuta.route('/api/massoterapeuta/agendamentos/confirmados', methods=['GET'])
@jwt_required()
def get_agendamentos_confirmados():
    """
    Retorna agendamentos com status 'confirmado' e 'concluido' do massoterapeuta logado.
    Histórico de sessões já realizadas ou confirmadas.
    """
    massoterapeuta_id = get_jwt_identity()
    try:
        agendamentos = listar_agendamentos_por_status(massoterapeuta_id, ['confirmado', 'concluido'])
        lista = [
            {
                "id": a["id"],
                "cliente_id": a["cliente_id"],
                "cliente_nome": a["cliente_nome"],
                "cliente_telefone": a.get("cliente_telefone", ""),
                "cliente_email": a.get("cliente_email", ""),
                "data_hora": str(a["data_hora"]),
                "sintomas": a.get("sintomas"),
                "status": a["status"],
                "criado_em": str(a["criado_em"])
            } for a in agendamentos
        ]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar agendamentos confirmados: {str(e)}"}), 500

@rota_massoterapeuta.route('/api/massoterapeuta/agendamentos', methods=['GET'])
@jwt_required()
def get_agendamentos():
    """
    Retorna TODOS os agendamentos do massoterapeuta logado.
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
                "cliente_telefone": a.get("cliente_telefone", ""),
                "cliente_email": a.get("cliente_email", ""),
                "data_hora": str(a["data_hora"]),
                "sintomas": a.get("sintomas"),
                "status": a["status"],
                "criado_em": str(a["criado_em"])
            } for a in agendamentos
        ]
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar agendamentos: {str(e)}"}), 500

@rota_massoterapeuta.route('/api/massoterapeuta/buscar-paciente', methods=['GET'])
@jwt_required()
def buscar_paciente():
    """
    Busca paciente por nome e retorna histórico completo de agendamentos.
    Query param: ?nome=João
    Retorna: dados do cliente + todos seus agendamentos com este massoterapeuta
    """
    massoterapeuta_id = get_jwt_identity()
    nome_busca = request.args.get('nome', '').strip()
    
    if not nome_busca:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório"}), 400
    
    try:
        resultado = buscar_paciente_com_historico(massoterapeuta_id, nome_busca)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": f"Erro ao buscar paciente: {str(e)}"}), 500

@rota_massoterapeuta.route('/api/massoterapeuta/me', methods=['PUT'])
@jwt_required()
def atualizar_perfil():
    """
    Atualiza nome e telefone do massoterapeuta logado.
    Email não pode ser alterado.
    """
    massoterapeuta_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        nome = data.get('nome')
        telefone = data.get('telefone')
        
        if not nome or not telefone:
            return jsonify({"erro": "Nome e telefone são obrigatórios"}), 400
            
        atualizar_conta(int(massoterapeuta_id), nome, telefone)
        return jsonify({"mensagem": "Perfil atualizado com sucesso"})
        
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar perfil: {str(e)}"}), 500

@rota_massoterapeuta.route('/api/massoterapeuta/agendamentos/<int:agendamento_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def atualizar_status_agendamento(agendamento_id):
    """
    Atualiza o status de um agendamento específico.
    Aceita: confirmado, cancelado, concluido
    """
    massoterapeuta_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        novo_status = data.get('status')
        
        if not novo_status:
            return jsonify({"erro": "Status é obrigatório"}), 400
            
        # Valida status permitidos (case insensitive)
        status_validos = ['pendente', 'marcado', 'confirmado', 'cancelado', 'concluido']
        novo_status = novo_status.lower()  # Converte para minúsculo
        if novo_status not in status_validos:
            return jsonify({"erro": f"Status inválido. Permitidos: {status_validos}"}), 400
            
        sucesso = atualizar_agendamento(agendamento_id, int(massoterapeuta_id), novo_status)
        
        if sucesso:
            return jsonify({"mensagem": f"Agendamento atualizado para '{novo_status}' com sucesso"})
        else:
            return jsonify({"erro": "Agendamento não encontrado ou você não tem permissão"}), 404
        
    except Exception as e:
        return jsonify({"erro": f"Erro ao atualizar agendamento: {str(e)}"}), 500

@rota_massoterapeuta.route('/api/massoterapeuta/agendamentos/<int:agendamento_id>/cancelar', methods=['POST'])
@jwt_required()
def cancelar_agendamento_com_notificacao(agendamento_id):
    """
    Cancela um agendamento com motivo e envia email de notificação.
    Body: { "motivo": "Motivo do cancelamento..." }
    """
    massoterapeuta_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('motivo'):
        return jsonify({"erro": "Campo 'motivo' é obrigatório"}), 400
    
    motivo = data.get('motivo', '').strip()
    
    if len(motivo) < 10:
        return jsonify({"erro": "O motivo deve ter pelo menos 10 caracteres"}), 400
    
    try:
        resultado = cancelar_agendamento_com_motivo(agendamento_id, massoterapeuta_id, motivo)
        
        if resultado['success']:
            return jsonify({
                "mensagem": resultado['mensagem'],
                "email_enviado": resultado.get('email_enviado', False),
                "detalhes": resultado.get('detalhes_email', '')
            })
        else:
            return jsonify({"erro": resultado['erro']}), 400
            
    except Exception as e:
        return jsonify({"erro": f"Erro ao cancelar agendamento: {str(e)}"}), 500

@rota_massoterapeuta.route('/api/massoterapeuta/clientes/<int:cliente_id>', methods=['DELETE'])
@jwt_required()
def excluir_cliente_por_massoterapeuta(cliente_id):
    """
    Permite ao massoterapeuta excluir um cliente do sistema.
    Apenas massoterapeutas podem realizar esta ação.
    """
    massoterapeuta_id = get_jwt_identity()
    
    try:
        resultado = excluir_cliente(cliente_id)
        
        if resultado:
            return jsonify({"mensagem": "Cliente excluído com sucesso"}), 200
        else:
            return jsonify({"erro": "Cliente não encontrado ou erro ao excluir"}), 404
            
    except Exception as e:
        return jsonify({"erro": f"Erro ao excluir cliente: {str(e)}"}), 500
