# ===== ENTRY POINT RAILWAY =====
import os
import sys

# Adiciona Back_end ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
back_end_dir = os.path.join(current_dir, 'Back_end')
sys.path.insert(0, back_end_dir)

# Imports das rotas do Back_end (sem imports relativos)
from rota_clientes import rota_clientes
from rota_massoterapeuta import rota_massoterapeuta  
from rota_whatsapp import rota_whatsapp
from rota_contato import rota_contato

# Flask e configurações
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Cria aplicação Flask
app = Flask(__name__)

# Configuração JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "minha_chave_super_secreta")
jwt = JWTManager(app)

# Configuração CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS(app, resources={r"/api/*": {"origins": [FRONTEND_URL, "http://localhost:5173"]}})

# Tratamento de erros
@app.errorhandler(422)
def handle_422(err):
    return jsonify({"erro": "Erro 422: " + str(err)}), 422

@app.errorhandler(NoAuthorizationError)
def handle_no_auth(err):
    return jsonify({"erro": "Token ausente ou inválido"}), 401

# Registra as rotas
app.register_blueprint(rota_clientes)
app.register_blueprint(rota_massoterapeuta)
app.register_blueprint(rota_whatsapp)
app.register_blueprint(rota_contato)

# Health check
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "API está funcionando!",
        "version": "1.0"
    })

# Execução
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )