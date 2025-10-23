import os
print("CWD:", os.getcwd())
print("Back_end contents:", os.listdir(os.path.join(os.getcwd(), "Back_end")))
# ===== IMPORTS =====
# Flask: Framework web para Python - cria o servidor HTTP
from flask import Flask, jsonify
# CORS: Permite que o frontend (React) se comunique com o backend
from flask_cors import CORS
# JWT: Sistema de autenticação por tokens (login seguro)
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
# dotenv: Carrega variáveis do arquivo .env
from dotenv import load_dotenv
import sys
import os

# Adiciona o diretório Back_end ao path para imports funcionarem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Rotas: Importa todas as URLs/endpoints da aplicação
from Back_end.rota_clientes import rota_clientes         # APIs para clientes
from Back_end.rota_massoterapeuta import rota_massoterapeuta  # APIs para massoterapeutas
from Back_end.rota_whatsapp import rota_whatsapp         # APIs para WhatsApp
from Back_end.rota_contato import rota_contato           # APIs para formulário de contato

# ===== CARREGAMENTO DE VARIÁVEIS DE AMBIENTE =====
load_dotenv()  # Carrega todas as variáveis do arquivo .env

# ===== CRIAÇÃO DA APLICAÇÃO =====
# Cria a instância principal do servidor Flask

app = Flask(__name__)

# Rota raiz para status do backend
@app.route("/")
def index():
    return "API Massoterapia HM rodando!", 200

# ===== CONFIGURAÇÃO DE SEGURANÇA =====
# 🔑 Chave secreta para assinar tokens JWT (senha do sistema)
# IMPORTANTE: Em produção, usar uma chave mais complexa e secreta
app.config["JWT_SECRET_KEY"] = "minha_chave_super_secreta"

# ===== INICIALIZAÇÃO DO JWT =====
# Ativa o sistema de autenticação por tokens na aplicação
jwt = JWTManager(app)

# ===== CONFIGURAÇÃO CORS =====
# Permite que o frontend React acesse as APIs (desenvolvimento e produção)
# Sem isso, o navegador bloqueia as requisições por segurança
import os
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS(app, resources={r"/api/*": {"origins": [FRONTEND_URL, "http://localhost:5173"]}})

# ===== TRATAMENTO DE ERROS =====
# Captura erros HTTP 422 (dados inválidos) e retorna JSON padronizado
@app.errorhandler(422)
def handle_422(err):
    return jsonify({"erro": "Erro 422: " + str(err)}), 422

# Captura erros de token inválido/ausente e retorna erro 401
@app.errorhandler(NoAuthorizationError)
def handle_no_auth(err):
    return jsonify({"erro": "Token ausente ou inválido"}), 401

# ===== REGISTRO DAS ROTAS =====
# Conecta todas as URLs/endpoints à aplicação principal
app.register_blueprint(rota_clientes)        # /api/clientes/*
app.register_blueprint(rota_massoterapeuta)  # /api/massoterapeuta/*
app.register_blueprint(rota_whatsapp)        # /api/whatsapp/*
app.register_blueprint(rota_contato)         # /api/contato/*

# ===== ROTA DE HEALTH CHECK =====
@app.route('/health')
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        "status": "healthy",
        "message": "API está funcionando!",
        "version": "1.0"
    })

# ===== EXECUÇÃO DO SERVIDOR =====
# Se este arquivo for executado diretamente, inicia o servidor
if __name__ == '__main__':
    # Configura porta para produção (Railway) ou desenvolvimento
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    
    app.run(
        host="0.0.0.0",  # Permite acesso externo (necessário para Railway)
        port=port,
        debug=debug
    )