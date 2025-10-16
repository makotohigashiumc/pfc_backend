#!/usr/bin/env python3
"""
Entry point para Railway
Importa e executa a aplicação Flask do Back_end
"""

import os
import sys

# Adiciona o diretório atual ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa a aplicação Flask do Back_end
from Back_end.app import app

if __name__ == '__main__':
    # Configura porta para Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)