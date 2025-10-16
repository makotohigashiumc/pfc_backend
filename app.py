# ===== ENTRY POINT RAILWAY =====
import os
import sys

# Caminho para o diretório Back_end
current_dir = os.path.dirname(os.path.abspath(__file__))
back_end_dir = os.path.join(current_dir, 'Back_end')

# Adiciona Back_end ao path E muda para o diretório
sys.path.insert(0, back_end_dir)
os.chdir(back_end_dir)

# Configura porta ANTES de importar
port = int(os.environ.get("PORT", 5000))
os.environ["PORT"] = str(port)

# Executa o Back_end/app.py diretamente
exec(open('app.py').read())