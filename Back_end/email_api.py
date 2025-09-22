def sendgrid_email_api_massoterapia(destinatario, assunto, conteudo):
    """
    Função de teste para envio de e-mail via SendGrid usando dados do .env.
    destinatario: e-mail de destino
    assunto: assunto do e-mail
    conteudo: texto do e-mail
    """
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [
            {"to": [{"email": destinatario}]}
        ],
        "from": {
            "email": SENDER_EMAIL,
            "name": SENDER_NAME
        },
        "subject": assunto,
        "content": [
            {"type": "text/plain", "value": conteudo}
        ]
    }
    response = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}")
    return response.status_code, response.text
import os
import requests
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  # Nova chave
SENDER_EMAIL = os.getenv("SENDER_EMAIL")          # Novo e-mail do remetente
SENDER_NAME = os.getenv("SENDER_NAME", "Massoterapia TCC")  # Nome do remetente
import os
import requests
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"

EMAIL_SECRET = os.getenv("EMAIL_SECRET", "supersecret")

def send_email(to_email, subject, content):
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [
            {"to": [{"email": to_email}]}
        ],
        "from": {
            "email": SENDER_EMAIL,
            "name": SENDER_NAME
        },
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": content}
        ]
    }
    response = requests.post(SENDGRID_URL, headers=headers, json=data)
    return response.status_code, response.text

# Função para gerar token de confirmação de e-mail
def generate_confirmation_token(email):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, EMAIL_SECRET, algorithm="HS256")
    return token

# Função para verificar token de confirmação
def verify_confirmation_token(token):
    try:
        payload = jwt.decode(token, EMAIL_SECRET, algorithms=["HS256"])
        return payload["email"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Função para enviar e-mail de confirmação
def send_confirmation_email(to_email):
    token = generate_confirmation_token(to_email)
    # Use o endereço local do frontend para testes
    confirm_url = f"http://localhost:5173/confirmar-email/{token}"
    subject = "Confirme seu e-mail"
    content = f"Olá! Clique no link para confirmar seu e-mail: {confirm_url}\nEste link expira em 24 horas."
    return send_email(to_email, subject, content)
