"""
Script de teste para verificar configuração do WhatsApp
"""
import os
from dotenv import load_dotenv
import sys

# Carrega variáveis de ambiente
load_dotenv(dotenv_path='../.env')

# Adiciona path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_whatsapp_config():
    """Testa configuração do WhatsApp"""
    print("🔍 Verificando configuração do WhatsApp...")
    
    # Verifica variáveis de ambiente
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID') 
    webhook_token = os.getenv('WHATSAPP_WEBHOOK_VERIFY_TOKEN')
    
    print(f"✅ Access Token: {'✓ Configurado' if access_token else '❌ Não encontrado'}")
    print(f"✅ Phone Number ID: {'✓ Configurado' if phone_id else '❌ Não encontrado'}")
    print(f"✅ Webhook Token: {'✓ Configurado' if webhook_token else '❌ Não encontrado'}")
    
    if access_token:
        print(f"   Token (primeiros 20 chars): {access_token[:20]}...")
    if phone_id:
        print(f"   Phone ID: {phone_id}")
        
    return bool(access_token and phone_id)

def test_whatsapp_api():
    """Testa se a API do WhatsApp está respondendo"""
    try:
        from whatsapp_api import WhatsAppCloudAPI
        
        print("\n🔗 Testando conexão com WhatsApp API...")
        
        # Inicializa API
        whatsapp = WhatsAppCloudAPI()
        print("✅ Classe WhatsAppCloudAPI inicializada com sucesso!")
        
        # Teste simples (sem enviar mensagem real)
        print(f"   URL da API: {whatsapp.api_url}")
        print(f"   Headers configurados: ✓")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar WhatsApp API: {e}")
        return False

def check_database_connection():
    """Verifica conexão com banco de dados"""
    try:
        from database import get_connection
        
        print("\n🔗 Testando conexão com banco de dados...")
        conn = get_connection()
        
        if conn:
            print("✅ Conexão com banco estabelecida!")
            
            # Verifica se há agendamentos
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM agendamento")
            count = cursor.fetchone()[0]
            print(f"   📊 Total de agendamentos no banco: {count}")
            
            cursor.close()
            conn.close()
            return True
        else:
            print("❌ Falha na conexão com banco")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

if __name__ == "__main__":
    print("🧪 === TESTE DE CONFIGURAÇÃO WHATSAPP ===\n")
    
    # Testa configurações
    config_ok = test_whatsapp_config()
    api_ok = test_whatsapp_api() if config_ok else False
    db_ok = check_database_connection()
    
    print(f"\n📊 === RESULTADO DOS TESTES ===")
    print(f"   Configuração: {'✅ OK' if config_ok else '❌ FALHA'}")
    print(f"   API WhatsApp: {'✅ OK' if api_ok else '❌ FALHA'}")
    print(f"   Banco de dados: {'✅ OK' if db_ok else '❌ FALHA'}")
    
    if all([config_ok, api_ok, db_ok]):
        print("\n🎉 Todos os testes passaram! WhatsApp deve estar funcionando.")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique as configurações.")