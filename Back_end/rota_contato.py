# ===== ROTA DE CONTATO =====
# Rota responsável por processar mensagens do formulário de contato
# Recebe dados do formulário e envia email para a clínica

# ===== IMPORTS =====
from flask import Blueprint, request, jsonify
from .email_api import send_email
import os
from dotenv import load_dotenv

# ===== CONFIGURAÇÕES =====
load_dotenv()

# Cria blueprint para organizar as rotas de contato
rota_contato = Blueprint('contato', __name__)

# Email da clínica que receberá as mensagens
EMAIL_CLINICA = "hmmassoterapia7@gmail.com"

# ===== ROTA: ENVIAR MENSAGEM DE CONTATO =====
@rota_contato.route('/api/contato', methods=['POST'])
def enviar_mensagem_contato():
    """
    Processa formulário de contato e envia email para a clínica
    
    Dados esperados (JSON):
    - nome: Nome completo do remetente
    - email: Email do remetente
    - telefone: Telefone do remetente (opcional)
    - assunto: Categoria da mensagem
    - mensagem: Conteúdo da mensagem
    
    Retorna:
    - JSON com status de sucesso/erro
    """
    try:
        # ===== RECEBIMENTO DOS DADOS =====
        dados = request.get_json()
        
        # Validação básica dos campos obrigatórios
        if not dados:
            return jsonify({"erro": "Dados não fornecidos"}), 400
            
        nome = dados.get('nome', '').strip()
        email = dados.get('email', '').strip()
        telefone = dados.get('telefone', '').strip()
        assunto = dados.get('assunto', '').strip()
        mensagem = dados.get('mensagem', '').strip()
        
        # Validação de campos obrigatórios
        if not nome:
            return jsonify({"erro": "Nome é obrigatório"}), 400
        if not email:
            return jsonify({"erro": "Email é obrigatório"}), 400
        if not assunto:
            return jsonify({"erro": "Assunto é obrigatório"}), 400
        if not mensagem:
            return jsonify({"erro": "Mensagem é obrigatória"}), 400
            
        # ===== MONTAGEM DO EMAIL =====
        # Assunto do email para a clínica
        assunto_email = f"Nova mensagem do site - {assunto}"
        
        # Conteúdo do email formatado
        conteudo_email = f"""
NOVA MENSAGEM RECEBIDA PELO SITE

====================================
DADOS DO CONTATO:
====================================
Nome: {nome}
Email: {email}
Telefone: {telefone if telefone else 'Não informado'}
Assunto: {assunto}

====================================
MENSAGEM:
====================================
{mensagem}

====================================
Esta mensagem foi enviada através do formulário de contato do site.
Para responder, utilize o email: {email}
        """
        
        # ===== ENVIO DO EMAIL =====
        status_code, response_text = send_email(
            to_email=EMAIL_CLINICA,
            subject=assunto_email,
            content=conteudo_email
        )
        
        # Verifica se o envio foi bem-sucedido
        if status_code == 202:  # SendGrid retorna 202 para sucesso
            return jsonify({
                "sucesso": True,
                "mensagem": "Mensagem enviada com sucesso! Entraremos em contato em breve."
            }), 200
        else:
            # Log do erro para debugging
            print(f"Erro no envio de email: Status {status_code}, Response: {response_text}")
            return jsonify({
                "erro": "Erro interno do servidor ao enviar email"
            }), 500
            
    except Exception as e:
        # Log do erro para debugging
        print(f"Erro no processamento da mensagem de contato: {str(e)}")
        return jsonify({
            "erro": "Erro interno do servidor"
        }), 500

# ===== ROTA: TESTE DE CONFIGURAÇÃO =====
@rota_contato.route('/api/contato/teste', methods=['GET'])
def teste_configuracao_email():
    """
    Rota para testar se a configuração de email está funcionando
    Envia um email de teste para a clínica
    """
    try:
        status_code, response_text = send_email(
            to_email=EMAIL_CLINICA,
            subject="Teste de Configuração - Sistema de Contato",
            content="Este é um email de teste para verificar se o sistema de contato está funcionando corretamente."
        )
        
        if status_code == 202:
            return jsonify({
                "sucesso": True,
                "mensagem": "Email de teste enviado com sucesso!"
            }), 200
        else:
            return jsonify({
                "erro": f"Falha no envio. Status: {status_code}",
                "detalhes": response_text
            }), 500
            
    except Exception as e:
        return jsonify({
            "erro": f"Erro no teste: {str(e)}"
        }), 500