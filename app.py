# ===== ENTRY POINT RAILWAY =====
import os
import sys

# Caminho para o diretório Back_end
current_dir = os.path.dirname(os.path.abspath(__file__))
back_end_dir = os.path.join(current_dir, 'Back_end')

# Muda para o diretório Back_end
os.chdir(back_end_dir)

# Executa a aplicação como módulo Python do Back_end
# Isso resolve TODOS os imports relativos
if __name__ == '__main__':
    # Configura porta do Railway
    port = os.environ.get("PORT", "5000")
    os.environ["PORT"] = port
    
    # Executa o app.py do Back_end diretamente
    sys.path.insert(0, back_end_dir)
    
    # Importa e executa o app do Back_end
    import app as backend_app
    
    # A variável Flask se chama 'app' dentro do módulo
    flask_app = backend_app.app
    flask_app.run(
        host="0.0.0.0",
        port=int(port),
        debug=False
    )