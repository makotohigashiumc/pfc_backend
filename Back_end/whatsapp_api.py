# ===== WHATSAPP CLOUD API INTEGRATION =====
"""
Módulo para integração com WhatsApp Cloud API da Meta
Funcionalidades:
- Envio de mensagens de texto
- Envio de templates
- Confirmações de agendamento
- Validação de webhooks
- Tratamento de respostas
"""

import os
import json
import requests
import hmac
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import phonenumbers
from phonenumbers import NumberParseException
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv(dotenv_path='../.env')

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppCloudAPI:
    """
    Classe principal para integração com WhatsApp Cloud API
    """
    
    def __init__(self):
        """Inicializa a classe com configurações da API"""
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.webhook_verify_token = os.getenv('WHATSAPP_WEBHOOK_VERIFY_TOKEN')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        
        if not all([self.access_token, self.phone_number_id]):
            raise ValueError("Variáveis de ambiente WHATSAPP_ACCESS_TOKEN e WHATSAPP_PHONE_NUMBER_ID são obrigatórias")
        
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def _format_phone(self, phone: str) -> str:
        """
        Formata número de telefone para padrão internacional
        Args:
            phone: Número de telefone em qualquer formato
        Returns:
            Número formatado no padrão internacional (55XXXXXXXXXXX)
        """
        try:
            # Remove caracteres não numéricos
            clean_phone = ''.join(filter(str.isdigit, phone))
            
            # Se não tem código do país, adiciona Brasil (55)
            if len(clean_phone) == 11 and clean_phone.startswith('9'):
                clean_phone = '55' + clean_phone
            elif len(clean_phone) == 10:
                clean_phone = '559' + clean_phone
            elif not clean_phone.startswith('55'):
                clean_phone = '55' + clean_phone
            
            # Validação usando phonenumbers
            parsed_number = phonenumbers.parse(f"+{clean_phone}", None)
            if phonenumbers.is_valid_number(parsed_number):
                return clean_phone
            else:
                raise ValueError(f"Número de telefone inválido: {phone}")
                
        except (NumberParseException, ValueError) as e:
            logger.error(f"Erro ao formatar telefone {phone}: {e}")
            raise ValueError(f"Formato de telefone inválido: {phone}")
    
    def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz requisição para a API do WhatsApp
        Args:
            payload: Dados da mensagem
        Returns:
            Resposta da API
        """
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response_data = response.json()
            
            if response.status_code == 200:
                logger.info(f"Mensagem enviada com sucesso: {response_data}")
                return {
                    'success': True,
                    'message_id': response_data.get('messages', [{}])[0].get('id'),
                    'data': response_data
                }
            else:
                logger.error(f"Erro ao enviar mensagem: {response.status_code} - {response_data}")
                return {
                    'success': False,
                    'error': response_data.get('error', {}).get('message', 'Erro desconhecido'),
                    'status_code': response.status_code
                }
                
        except requests.RequestException as e:
            logger.error(f"Erro de conexão ao enviar mensagem: {e}")
            return {
                'success': False,
                'error': f"Erro de conexão: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar mensagem: {e}")
            return {
                'success': False,
                'error': f"Erro inesperado: {str(e)}"
            }
    
    def send_message(self, to_number: str, message_text: str) -> Dict[str, Any]:
        """
        Envia mensagem de texto simples
        Args:
            to_number: Número de telefone do destinatário
            message_text: Texto da mensagem
        Returns:
            Resultado do envio
        """
        try:
            formatted_phone = self._format_phone(to_number)
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": formatted_phone,
                "type": "text",
                "text": {
                    "body": message_text
                }
            }
            
            return self._make_request(payload)
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_template_message(self, to_number: str, template_name: str, 
                            language: str = "pt_BR", components: Optional[list] = None) -> Dict[str, Any]:
        """
        Envia mensagem usando template aprovado
        Args:
            to_number: Número de telefone do destinatário
            template_name: Nome do template aprovado no Facebook
            language: Código do idioma (default: pt_BR)
            components: Parâmetros do template
        Returns:
            Resultado do envio
        """
        try:
            formatted_phone = self._format_phone(to_number)
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": formatted_phone,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language
                    },
                    "components": components or []
                }
            }
            
            return self._make_request(payload)
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_appointment_confirmation(self, phone: str, cliente_nome: str, 
                                    data_hora: datetime, massoterapeuta_nome: str) -> Dict[str, Any]:
        """
        Confirma agendamento via WhatsApp
        Args:
            phone: Telefone do cliente
            cliente_nome: Nome do cliente
            data_hora: Data e hora do agendamento
            massoterapeuta_nome: Nome do massoterapeuta
        Returns:
            Resultado do envio
        """
        data_formatada = data_hora.strftime("%d/%m/%Y às %H:%M")
        
        message = f"""🏥 *HM Massoterapia*

✅ *Agendamento Solicitado*

Olá {cliente_nome}!

Sua solicitação de agendamento foi recebida:

📅 Data: {data_formatada}
👨‍⚕️ Massoterapeuta: {massoterapeuta_nome}

⏳ Status: Aguardando confirmação da clínica

Você receberá uma nova mensagem quando o agendamento for confirmado.

📞 Dúvidas? Entre em contato: (11) 97610-1010"""
        
        return self.send_message(phone, message.strip())
    
    def send_appointment_approved(self, phone: str, cliente_nome: str, 
                                data_hora: datetime, massoterapeuta_nome: str) -> Dict[str, Any]:
        """
        Notifica aprovação do agendamento
        Args:
            phone: Telefone do cliente
            cliente_nome: Nome do cliente
            data_hora: Data e hora do agendamento
            massoterapeuta_nome: Nome do massoterapeuta
        Returns:
            Resultado do envio
        """
        data_formatada = data_hora.strftime("%d/%m/%Y às %H:%M")
        
        message = f"""🏥 *HM Massoterapia*

✅ *Agendamento Confirmado*

Olá {cliente_nome}!

Seu agendamento foi confirmado:

📅 Data: {data_formatada}
👨‍⚕️ Massoterapeuta: {massoterapeuta_nome}

📍 Endereço: [Inserir endereço da clínica]

⚠️ Importante:
• Chegue 10 minutos antes
• Traga documento com foto
• Em caso de cancelamento, avise com 24h de antecedência

📞 Contato: (11) 97610-1010"""
        
        return self.send_message(phone, message.strip())
    
    def send_appointment_reminder(self, phone: str, cliente_nome: str, 
                                data_hora: datetime, massoterapeuta_nome: str) -> Dict[str, Any]:
        """
        Envia lembrete do agendamento (24h antes)
        Args:
            phone: Telefone do cliente
            cliente_nome: Nome do cliente
            data_hora: Data e hora do agendamento
            massoterapeuta_nome: Nome do massoterapeuta
        Returns:
            Resultado do envio
        """
        data_formatada = data_hora.strftime("%d/%m/%Y às %H:%M")
        
        message = f"""🏥 *HM Massoterapia*

⏰ *Lembrete de Agendamento*

Olá {cliente_nome}!

Você tem um agendamento amanhã:

📅 Data: {data_formatada}
👨‍⚕️ Massoterapeuta: {massoterapeuta_nome}

📍 Endereço: [Inserir endereço da clínica]

⚠️ Lembre-se:
• Chegue 10 minutos antes
• Traga documento com foto

📞 Para reagendar ou cancelar: (11) 97610-1010"""
        
        return self.send_message(phone, message.strip())
    
    def verify_webhook(self, verify_token: str, challenge: str) -> Optional[str]:
        """
        Verifica webhook do WhatsApp
        Args:
            verify_token: Token de verificação recebido
            challenge: Desafio enviado pelo Facebook
        Returns:
            Challenge se token for válido, None caso contrário
        """
        if verify_token == self.webhook_verify_token:
            logger.info("Webhook verificado com sucesso")
            return challenge
        else:
            logger.warning(f"Token de verificação inválido: {verify_token}")
            return None
    
    def verify_signature(self, payload: str, signature: str) -> bool:
        """
        Verifica assinatura do webhook para segurança
        Args:
            payload: Dados recebidos do webhook
            signature: Assinatura SHA256 do Facebook
        Returns:
            True se assinatura for válida
        """
        if not self.app_secret:
            logger.warning("FACEBOOK_APP_SECRET não configurado - verificação de assinatura desabilitada")
            return True
        
        try:
            expected_signature = hmac.new(
                self.app_secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Remove 'sha256=' do início da assinatura
            received_signature = signature.replace('sha256=', '')
            
            is_valid = hmac.compare_digest(expected_signature, received_signature)
            
            if not is_valid:
                logger.warning("Assinatura do webhook inválida")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Erro ao verificar assinatura: {e}")
            return False
    
    def process_webhook_message(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa mensagens recebidas via webhook
        Args:
            webhook_data: Dados do webhook do WhatsApp
        Returns:
            Dados processados da mensagem
        """
        try:
            # Extrai dados da mensagem
            entry = webhook_data.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            
            if 'messages' in value:
                message = value['messages'][0]
                contact = value.get('contacts', [{}])[0]
                
                return {
                    'message_id': message.get('id'),
                    'from_number': message.get('from'),
                    'contact_name': contact.get('profile', {}).get('name'),
                    'message_type': message.get('type'),
                    'text': message.get('text', {}).get('body'),
                    'timestamp': datetime.fromtimestamp(int(message.get('timestamp')))
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem do webhook: {e}")
            return {}

# Instância global da API (singleton pattern)  
# Criada sob demanda para evitar erro na importação
whatsapp_api = None

def get_whatsapp_api():
    """
    Retorna instância singleton da WhatsApp API
    Cria sob demanda para evitar erros de importação
    """
    global whatsapp_api
    if whatsapp_api is None:
        whatsapp_api = WhatsAppCloudAPI()
    return whatsapp_api