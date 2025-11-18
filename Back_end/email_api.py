import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "Massoterapia TCC")
EMAIL_SECRET = os.getenv("EMAIL_SECRET", "supersecret")

# ===== FUNÇÃO PRINCIPAL: ENVIAR EMAIL =====
def send_email(to_email, subject, content):
    """
    Envia email usando SendGrid (primário) ou Gmail SMTP (fallback)
    
    Parâmetros:
    - to_email: Email do destinatário
    - subject: Assunto do email
    - content: Conteúdo em texto puro
    
    Retorna:
    - Tupla (status_code, response_text)
    """
    if SENDGRID_API_KEY and SENDGRID_API_KEY != "SG.xxxxxx_SUBSTITUA_PELA_CHAVE_REAL_xxxx":
        try:
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
            response = requests.post(SENDGRID_URL, json=data, headers=headers)
            if response.status_code == 202:
                return response.status_code, response.text
            else:
                print(f"SendGrid falhou (Status: {response.status_code}), tentando Gmail SMTP...")
        except Exception as e:
            print(f"Erro no SendGrid: {str(e)}, tentando Gmail SMTP...")
    
    if GMAIL_USER and GMAIL_PASSWORD:
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{SENDER_NAME} <{GMAIL_USER}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(content, 'plain'))
            
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            
            text = msg.as_string()
            server.sendmail(GMAIL_USER, to_email, text)
            server.quit()
            
            print("Email enviado com sucesso via Gmail SMTP")
            return 202, "Email enviado via Gmail SMTP (fallback)"
            
        except Exception as e:
            print(f"Erro no Gmail SMTP: {str(e)}")
            return 500, f"Erro no envio: {str(e)}"
    
    return 500, "Falha no envio: SendGrid e Gmail SMTP indisponíveis"

# ===== GERAÇÃO DE TOKEN DE CONFIRMAÇÃO =====
def generate_confirmation_token(email):
    """
    Gera token JWT para confirmação de email ou recuperação de senha
    
    Parâmetros:
    - email: Email do usuário
    
    Retorna:
    - Token JWT válido por 24 horas
    """
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, EMAIL_SECRET, algorithm="HS256")
    return token

# ===== VERIFICAÇÃO DE TOKEN =====
def verify_confirmation_token(token):
    """
    Verifica se token JWT é válido e não expirou
    
    Parâmetros:
    - token: Token JWT a ser verificado
    
    Retorna:
    - Email do usuário se válido, None se inválido/expirado
    """
    try:
        payload = jwt.decode(token, EMAIL_SECRET, algorithms=["HS256"])
        return payload["email"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ===== ENVIO DE EMAIL DE CONFIRMAÇÃO =====
def send_confirmation_email(to_email):
    """
    Envia email de confirmação para ativação de conta
    
    Parâmetros:
    - to_email: Email do destinatário
    
    Retorna:
    - Tupla (status_code, response_text) do envio
    """
    token = generate_confirmation_token(to_email)
    env = os.getenv("ENV", "prod")
    if env == "local":
        frontend_url = os.getenv("FRONTEND_URL_LOCAL", "http://localhost:5173")
    else:
        frontend_url = os.getenv("FRONTEND_URL_PROD", "https://hmmassoterapia.com.br")
    confirm_url = f"{frontend_url}/confirmar-email/{token}"
    subject = "Confirme seu e-mail"
    content = f"Olá! Clique no link para confirmar seu e-mail: {confirm_url}\nEste link expira em 24 horas."
    return send_email(to_email, subject, content)

# ===== FUNÇÃO LEGADA - PARA COMPATIBILIDADE =====
def sendgrid_email_api_massoterapia(destinatario, assunto, conteudo):
    """
    Função legada para compatibilidade com código existente
    Simplesmente chama a função send_email com novos nomes
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
