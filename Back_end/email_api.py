# ===== COMENTÁRIOS FORAM RETIRADOS - CONTEÚDO DUPLICADO =====

# ===== IMPORTS NECESSÁRIOS =====
import os  # Para acessar variáveis de ambiente do sistema
import requests  # Para fazer requisições HTTP (SendGrid API)
import smtplib  # Para envio via SMTP (Gmail)
from email.mime.text import MIMEText  # Para formatar emails SMTP
from email.mime.multipart import MIMEMultipart  # Para emails multipart
from dotenv import load_dotenv  # Carrega variáveis do arquivo .env
import jwt  # Para gerar e verificar tokens JWT
from datetime import datetime, timedelta  # Manipulação de datas

# ===== CARREGAMENTO DE CONFIGURAÇÕES =====
load_dotenv()  # Carrega todas as variáveis do arquivo .env

# ===== CONFIGURAÇÕES DO SENDGRID =====
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  # Chave da API SendGrid
SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"  # URL da API SendGrid

# ===== CONFIGURAÇÕES DO GMAIL SMTP (FALLBACK) =====
GMAIL_USER = os.getenv("GMAIL_USER")  # Email Gmail para envio
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # Senha de app do Gmail
SMTP_SERVER = "smtp.gmail.com"  # Servidor SMTP do Gmail
SMTP_PORT = 587  # Porta SMTP (TLS)

# ===== CONFIGURAÇÕES DE EMAIL =====
SENDER_EMAIL = os.getenv("SENDER_EMAIL")  # Email remetente (configurado no SendGrid)
SENDER_NAME = os.getenv("SENDER_NAME", "Massoterapia TCC")  # Nome do remetente
EMAIL_SECRET = os.getenv("EMAIL_SECRET", "supersecret")  # Chave secreta para tokens JWT

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
    # Tenta enviar via SendGrid primeiro
    if SENDGRID_API_KEY and SENDGRID_API_KEY != "SG.xxxxxx_SUBSTITUA_PELA_CHAVE_REAL_xxxx":
        try:
            headers = {  # Cabeçalhos da requisição HTTP
                "Authorization": f"Bearer {SENDGRID_API_KEY}",  # Token de autenticação
                "Content-Type": "application/json"  # Tipo de conteúdo JSON
            }
            data = {  # Estrutura dos dados do email
                "personalizations": [  # Lista de destinatários
                    {"to": [{"email": to_email}]}  # Email do destinatário
                ],
                "from": {  # Dados do remetente
                    "email": SENDER_EMAIL,  # Email remetente
                    "name": SENDER_NAME  # Nome remetente
                },
                "subject": subject,  # Assunto do email
                "content": [  # Lista de conteúdos
                    {"type": "text/plain", "value": content}  # Conteúdo em texto puro
                ]
            }
            response = requests.post(SENDGRID_URL, json=data, headers=headers)  # Faz requisição POST
            if response.status_code == 202:  # SendGrid retorna 202 para sucesso
                return response.status_code, response.text
            else:
                print(f"SendGrid falhou (Status: {response.status_code}), tentando Gmail SMTP...")
        except Exception as e:
            print(f"Erro no SendGrid: {str(e)}, tentando Gmail SMTP...")
    
    # Fallback para Gmail SMTP
    if GMAIL_USER and GMAIL_PASSWORD:
        try:
            # Cria mensagem
            msg = MIMEMultipart()
            msg['From'] = f"{SENDER_NAME} <{GMAIL_USER}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Adiciona corpo do email
            msg.attach(MIMEText(content, 'plain'))
            
            # Conecta ao servidor SMTP
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # Inicia TLS
            server.login(GMAIL_USER, GMAIL_PASSWORD)  # Faz login
            
            # Envia email
            text = msg.as_string()
            server.sendmail(GMAIL_USER, to_email, text)
            server.quit()  # Fecha conexão
            
            print("Email enviado com sucesso via Gmail SMTP")
            return 202, "Email enviado via Gmail SMTP (fallback)"
            
        except Exception as e:
            print(f"Erro no Gmail SMTP: {str(e)}")
            return 500, f"Erro no envio: {str(e)}"
    
    # Se ambos falharam
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
    payload = {  # Dados do token
        "email": email,  # Email do usuário
        "exp": datetime.utcnow() + timedelta(hours=24)  # Expira em 24 horas
    }
    token = jwt.encode(payload, EMAIL_SECRET, algorithm="HS256")  # Gera token JWT
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
    try:  # Tenta verificar o token
        payload = jwt.decode(token, EMAIL_SECRET, algorithms=["HS256"])  # Decodifica token
        return payload["email"]  # Retorna email do payload
    except jwt.ExpiredSignatureError:  # Se token expirou
        return None  # Retorna nulo
    except jwt.InvalidTokenError:  # Se token é inválido
        return None  # Retorna nulo

# ===== ENVIO DE EMAIL DE CONFIRMAÇÃO =====
def send_confirmation_email(to_email):
    """
    Envia email de confirmação para ativação de conta
    
    Parâmetros:
    - to_email: Email do destinatário
    
    Retorna:
    - Tupla (status_code, response_text) do envio
    """
    token = generate_confirmation_token(to_email)  # Gera token único
    # Monta URL de confirmação apontando para o frontend
    env = os.getenv("ENV", "prod")
    if env == "local":
        frontend_url = os.getenv("FRONTEND_URL_LOCAL", "http://localhost:5173")
    else:
        frontend_url = os.getenv("FRONTEND_URL_PROD", "https://hmmassoterapia.com.br")
    confirm_url = f"{frontend_url}/confirmar-email/{token}"
    subject = "Confirme seu e-mail"  # Assunto do email
    content = f"Olá! Clique no link para confirmar seu e-mail: {confirm_url}\nEste link expira em 24 horas."  # Conteúdo
    return send_email(to_email, subject, content)  # Envia email

# ===== FUNÇÃO LEGADA - PARA COMPATIBILIDADE =====
def sendgrid_email_api_massoterapia(destinatario, assunto, conteudo):
    """
    Função legada para compatibilidade com código existente
    Simplesmente chama a função send_email com novos nomes
    """
    headers = {  # Cabeçalhos HTTP
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {  # Dados do email
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
    response = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)  # Envia email
    print(f"Status: {response.status_code}")  # Log do status
    print(f"Resposta: {response.text}")  # Log da resposta
    return response.status_code, response.text  # Retorna status e resposta
