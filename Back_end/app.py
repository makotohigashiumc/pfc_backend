import os
# ===== IMPORTS =====
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Back_end.rota_clientes import rota_clientes
from Back_end.rota_massoterapeuta import rota_massoterapeuta
from Back_end.rota_contato import rota_contato

# ===== CARREGAMENTO DE VARIÁVEIS DE AMBIENTE =====
load_dotenv()

# ===== CRIAÇÃO DA APLICAÇÃO =====
app = Flask(__name__)

@app.route("/")
def index():
    return "API Massoterapia HM rodando!", 200

# ===== CONFIGURAÇÃO DE SEGURANÇA =====
app.config["JWT_SECRET_KEY"] = "minha_chave_super_secreta"

# ===== INICIALIZAÇÃO DO JWT =====
jwt = JWTManager(app)

# ===== CONFIGURAÇÃO CORS =====
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS(app, resources={r"/api/*": {"origins": [
    FRONTEND_URL,
    "http://localhost:5173",
    "https://pfc-frontend-delta.vercel.app",
    "https://hmmassoterapia.com.br",
    "https://www.hmmassoterapia.com.br"
]}})

# ===== TRATAMENTO DE ERROS =====
@app.errorhandler(422)
def handle_422(err):
    return jsonify({"erro": "Erro 422: " + str(err)}), 422

@app.errorhandler(NoAuthorizationError)
def handle_no_auth(err):
    return jsonify({"erro": "Token ausente ou inválido"}), 401

# ===== REGISTRO DAS ROTAS =====
app.register_blueprint(rota_clientes)
app.register_blueprint(rota_massoterapeuta)
app.register_blueprint(rota_contato)

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
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )