# ===== IMPORTS =====
# os: Para acessar variáveis de ambiente do sistema
import os
# dotenv: Carrega variáveis do arquivo .env (senhas, URLs de banco, etc.)
from dotenv import load_dotenv
# psycopg2: Driver para conectar Python com PostgreSQL
import psycopg2
from psycopg2 import OperationalError

# ===== CARREGAMENTO DE CONFIGURAÇÕES =====
# Carrega todas as variáveis do arquivo .env para uso seguro
load_dotenv()

def get_connection():
    """
    FUNÇÃO PRINCIPAL: Conecta ao banco de dados PostgreSQL
    
    Como funciona:
    1. Pega a URL do banco do arquivo .env
    2. Tenta conectar com SSL (segurança)
    3. Se falhar, tenta sem SSL
    4. Retorna a conexão ou None se falhar
    """
    try:
        # ===== OBTER URL DO BANCO =====
        # Busca a URL de conexão nas variáveis de ambiente
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            print("❌ Erro: DATABASE_URL não encontrada no arquivo .env")
            return None
            
        # ===== TENTATIVA DE CONEXÃO COM SSL =====
        print(f"🔗 Tentando conectar ao banco...")
        # sslmode='require': Força conexão segura (criptografada)
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        print("✅ Conexão estabelecida com sucesso!")
        return conn
        
    except OperationalError as e:
        print(f"❌ Erro de conexão ao banco de dados: {e}")
        
        # ===== TENTATIVA ALTERNATIVA SEM SSL =====
        # Se SSL falhar, tenta conectar sem criptografia
        try:
            print("🔄 Tentando conectar sem SSL...")
            conn = psycopg2.connect(DATABASE_URL, sslmode='disable')
            print("✅ Conexão estabelecida sem SSL!")
            return conn
        except Exception as e2:
            print(f"❌ Erro mesmo sem SSL: {e2}")
            return None
            
    except Exception as e:
        print(f"❌ Erro geral ao conectar: {e}")
        return None

def test_connection():
    """
    FUNÇÃO DE TESTE: Verifica se a conexão está funcionando
    
    Útil para:
    - Testar configuração do banco
    - Debugar problemas de conexão
    - Verificar se .env está correto
    """
    # Tenta obter uma conexão
    conn = get_connection()
    if conn:
        print("Conexão ao Supabase bem-sucedida!")
        # IMPORTANTE: Sempre fechar conexão após usar
        conn.close()
    else:
        print("Falha na conexão ao banco.")

# ===== EXECUÇÃO DIRETA =====
# Se este arquivo for executado diretamente, testa a conexão
if __name__ == "__main__":
    test_connection()
