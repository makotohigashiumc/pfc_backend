from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from .rota_clientes import rota_clientes
from .rota_massoterapeuta import rota_massoterapeuta

app = Flask(__name__)

# 🔑 chave secreta usada para assinar os tokens (troque por algo mais seguro em produção!)
app.config["JWT_SECRET_KEY"] = "minha_chave_super_secreta"

# inicializa o JWT
jwt = JWTManager(app)

# Permitir todos os endpoints /api/* para o frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Handlers para erros JWT e 422
@app.errorhandler(422)
def handle_422(err):
    return jsonify({"erro": "Erro 422: " + str(err)}), 422

@app.errorhandler(NoAuthorizationError)
def handle_no_auth(err):
    return jsonify({"erro": "Token ausente ou inválido"}), 401

# registra as rotas
app.register_blueprint(rota_clientes)
app.register_blueprint(rota_massoterapeuta)

if __name__ == '__main__':
    app.run(debug=True)