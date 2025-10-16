#!/usr/bin/env python3
"""
Entry point para Railway
Importa e executa a aplicação Flask do Back_end
"""

import os
import sys

# Adiciona o diretório atual ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'Back_end'))

try:
    # Tenta import relativo primeiro
    from Back_end.app import app
except ImportError:
    try:
        # Se falhar, tenta import direto
        import Back_end.app as backend_app
        app = backend_app.app
    except ImportError:
        # Último recurso: adiciona Back_end ao path e importa
        sys.path.append(os.path.join(current_dir, 'Back_end'))
        import app as flask_app
        app = flask_app.app

if __name__ == '__main__':
    # Configura porta para Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)