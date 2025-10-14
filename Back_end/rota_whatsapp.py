"""
Rotas para integração com WhatsApp Cloud API
Gerencia webhooks e envio de mensagens
"""

from flask import Blueprint, request, jsonify
import logging

# Import condicional para funcionar tanto como módulo quanto executado diretamente
try:
    from .whatsapp_api import get_whatsapp_api
except ImportError:
    from whatsapp_api import get_whatsapp_api

# Configuração de logging
logger = logging.getLogger(__name__)

# Cria blueprint para rotas do WhatsApp
rota_whatsapp = Blueprint('whatsapp', __name__, url_prefix='/api/whatsapp')

@rota_whatsapp.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Verificação do webhook do WhatsApp (chamada inicial do Facebook)
    """
    try:
        # Parâmetros enviados pelo Facebook para verificação
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        logger.info(f"Verificação de webhook recebida - Mode: {mode}, Token: {token}")
        
        if mode == 'subscribe':
            # Verifica token de verificação
            whatsapp = get_whatsapp_api()
            verified_challenge = whatsapp.verify_webhook(token, challenge)
            
            if verified_challenge:
                logger.info("Webhook verificado com sucesso")
                return verified_challenge, 200
            else:
                logger.warning("Token de verificação inválido")
                return jsonify({"erro": "Token de verificação inválido"}), 403
        else:
            logger.warning(f"Modo de verificação inválido: {mode}")
            return jsonify({"erro": "Modo inválido"}), 400
            
    except Exception as e:
        logger.error(f"Erro na verificação do webhook: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500

@rota_whatsapp.route('/webhook', methods=['POST'])
def receive_webhook():
    """
    Recebe mensagens e eventos do WhatsApp via webhook
    """
    try:
        # Verifica assinatura (segurança)
        signature = request.headers.get('X-Hub-Signature-256', '')
        payload = request.get_data(as_text=True)
        
        whatsapp = get_whatsapp_api()
        
        if not whatsapp.verify_signature(payload, signature):
            logger.warning("Assinatura do webhook inválida")
            return jsonify({"erro": "Assinatura inválida"}), 403
        
        # Processa dados do webhook
        webhook_data = request.get_json()
        
        if not webhook_data:
            logger.warning("Dados do webhook vazios")
            return jsonify({"erro": "Dados vazios"}), 400
        
        # Processa mensagem recebida
        message_data = whatsapp.process_webhook_message(webhook_data)
        
        if message_data:
            logger.info(f"Mensagem recebida de {message_data.get('from_number')}: {message_data.get('text')}")
            
            # Aqui você pode adicionar lógica personalizada:
            # - Salvar mensagem no banco de dados
            # - Processar comandos automáticos
            # - Enviar respostas automáticas
            # - Notificar massoterapeutas sobre novas mensagens
            
            # Exemplo de resposta automática simples
            if message_data.get('text', '').lower() in ['oi', 'olá', 'hello']:
                whatsapp.send_message(
                    message_data['from_number'],
                    "Olá! Obrigado por entrar em contato. Em breve nossa equipe retornará sua mensagem! 😊"
                )
        
        # Sempre retorna 200 para confirmar recebimento
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        # Mesmo com erro, retorna 200 para não reenviar
        return jsonify({"status": "error"}), 200

@rota_whatsapp.route('/send-message', methods=['POST'])
def send_message():
    """
    API para envio de mensagens via WhatsApp
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        # Validação dos campos obrigatórios
        to_number = data.get('to_number')
        message = data.get('message')
        
        if not to_number or not message:
            return jsonify({"erro": "Campos 'to_number' e 'message' são obrigatórios"}), 400
        
        # Envia mensagem
        whatsapp = get_whatsapp_api()
        resultado = whatsapp.send_message(to_number, message)
        
        if resultado['success']:
            return jsonify({
                "success": True,
                "message": "Mensagem enviada com sucesso",
                "message_id": resultado.get('message_id')
            }), 200
        else:
            return jsonify({
                "success": False,
                "erro": resultado.get('error')
            }), 400
            
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem via API: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500

@rota_whatsapp.route('/send-template', methods=['POST'])
def send_template():
    """
    API para envio de templates do WhatsApp
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        # Validação dos campos obrigatórios
        to_number = data.get('to_number')
        template_name = data.get('template_name')
        parameters = data.get('parameters', [])
        
        if not to_number or not template_name:
            return jsonify({"erro": "Campos 'to_number' e 'template_name' são obrigatórios"}), 400
        
        # Envia template
        whatsapp = get_whatsapp_api()
        resultado = whatsapp.send_template(to_number, template_name, parameters)
        
        if resultado['success']:
            return jsonify({
                "success": True,
                "message": "Template enviado com sucesso",
                "message_id": resultado.get('message_id')
            }), 200
        else:
            return jsonify({
                "success": False,
                "erro": resultado.get('error')
            }), 400
            
    except Exception as e:
        logger.error(f"Erro ao enviar template via API: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500

@rota_whatsapp.route('/status', methods=['GET'])
def whatsapp_status():
    """
    Verifica status da integração WhatsApp
    """
    try:
        # Testa se as configurações estão corretas
        import os
        
        config_status = {
            "access_token": bool(os.getenv('WHATSAPP_ACCESS_TOKEN')),
            "phone_number_id": bool(os.getenv('WHATSAPP_PHONE_NUMBER_ID')),
            "webhook_token": bool(os.getenv('WHATSAPP_WEBHOOK_VERIFY_TOKEN')),
            "app_secret": bool(os.getenv('FACEBOOK_APP_SECRET'))
        }
        
        all_configured = all(config_status.values())
        
        return jsonify({
            "status": "healthy" if all_configured else "partial",
            "message": "WhatsApp API configurado" if all_configured else "Configuração incompleta",
            "config": config_status
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao verificar status: {e}")
        return jsonify({
            "status": "error",
            "message": f"Erro: {str(e)}"
        }), 500