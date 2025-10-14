"""
Sistema de Lembretes Automáticos via WhatsApp
Envia lembretes 24h antes dos agendamentos confirmados
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv(dotenv_path='../.env')

# Adiciona o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from database import get_connection
from whatsapp_api import get_whatsapp_api

def enviar_lembretes_diarios():
    """
    Função para enviar lembretes automáticos
    Deve ser executada diariamente via cron job ou task scheduler
    """
    print("🔄 Iniciando envio de lembretes automáticos...")
    
    # Data/hora de amanhã (24h a partir de agora)
    amanha_inicio = datetime.now() + timedelta(days=1)
    amanha_inicio = amanha_inicio.replace(hour=0, minute=0, second=0, microsecond=0)
    amanha_fim = amanha_inicio.replace(hour=23, minute=59, second=59)
    
    conn = get_connection()
    if not conn:
        print("❌ Erro: Não foi possível conectar ao banco de dados")
        return
    
    cursor = None
    lembretes_enviados = 0
    
    try:
        cursor = conn.cursor()
        
        # Busca agendamentos confirmados para amanhã
        cursor.execute("""
            SELECT a.id, a.data_hora, c.nome, c.telefone, m.nome as massoterapeuta_nome, a.sintomas
            FROM agendamento a
            JOIN cliente c ON a.cliente_id = c.id  
            JOIN massoterapeuta m ON a.massoterapeuta_id = m.id
            WHERE a.status IN ('confirmado', 'marcado')
            AND a.data_hora BETWEEN %s AND %s
            AND c.telefone IS NOT NULL
            ORDER BY a.data_hora
        """, (amanha_inicio, amanha_fim))
        
        agendamentos = cursor.fetchall()
        
        print(f"📋 Encontrados {len(agendamentos)} agendamentos para amanhã")
        
        for agendamento in agendamentos:
            agendamento_id = agendamento[0]
            data_hora = agendamento[1]
            nome_cliente = agendamento[2]
            telefone_cliente = agendamento[3]
            massoterapeuta_nome = agendamento[4]
            sintomas = agendamento[5]
            
            try:
                # Formatar data e hora
                if isinstance(data_hora, str):
                    data_hora = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
                
                data_formatada = data_hora.strftime("%d/%m/%Y")
                hora_formatada = data_hora.strftime("%H:%M")
                
                # Enviar lembrete
                whatsapp = get_whatsapp_api()
                resultado = whatsapp.send_appointment_reminder(
                    phone=telefone_cliente,
                    cliente_nome=nome_cliente,
                    data_hora=datetime.strptime(str(data_hora), "%Y-%m-%d %H:%M:%S"),
                    massoterapeuta_nome=massoterapeuta_nome
                )
                
                if resultado['success']:
                    lembretes_enviados += 1
                    print(f"✅ Lembrete enviado para {nome_cliente}: {resultado.get('message_id')}")
                    
                    # Opcional: Marcar no banco que o lembrete foi enviado
                    # cursor.execute("UPDATE agendamento SET lembrete_enviado = TRUE WHERE id = %s", (agendamento_id,))
                    
                else:
                    print(f"❌ Erro ao enviar lembrete para {nome_cliente}: {resultado.get('error')}")
                    
            except Exception as e:
                print(f"❌ Erro ao processar agendamento {agendamento_id}: {e}")
                continue
        
        # conn.commit()  # Descomente se adicionar campo lembrete_enviado
        
        print(f"🎉 Processo concluído: {lembretes_enviados}/{len(agendamentos)} lembretes enviados")
        
    except Exception as e:
        print(f"❌ Erro geral no envio de lembretes: {e}")
        
    finally:
        if cursor:
            cursor.close()
        conn.close()

def enviar_lembrete_individual(agendamento_id):
    """
    Envia lembrete para um agendamento específico
    Útil para testes ou reenvios manuais
    """
    conn = get_connection()
    if not conn:
        print("❌ Erro: Não foi possível conectar ao banco de dados")
        return False
    
    cursor = None
    
    try:
        cursor = conn.cursor()
        
        # Busca dados do agendamento
        cursor.execute("""
            SELECT a.data_hora, c.nome, c.telefone, m.nome as massoterapeuta_nome
            FROM agendamento a
            JOIN cliente c ON a.cliente_id = c.id
            JOIN massoterapeuta m ON a.massoterapeuta_id = m.id  
            WHERE a.id = %s AND a.status IN ('confirmado', 'marcado')
        """, (agendamento_id,))
        
        agendamento = cursor.fetchone()
        
        if not agendamento:
            print(f"❌ Agendamento {agendamento_id} não encontrado ou não confirmado")
            return False
            
        data_hora = agendamento[0]
        nome_cliente = agendamento[1] 
        telefone_cliente = agendamento[2]
        massoterapeuta_nome = agendamento[3]
        
        if not telefone_cliente:
            print(f"❌ Cliente {nome_cliente} sem telefone cadastrado")
            return False
            
        # Formatar data e hora
        if isinstance(data_hora, str):
            data_hora = datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")
            
        data_formatada = data_hora.strftime("%d/%m/%Y às %H:%M")
        
        # Enviar lembrete
        whatsapp = get_whatsapp_api()
        resultado = whatsapp.send_appointment_reminder(
            phone=telefone_cliente,
            cliente_nome=nome_cliente,
            data_hora=datetime.now() + timedelta(days=1),
            massoterapeuta_nome=massoterapeuta_nome
        )
        
        if resultado['success']:
            print(f"✅ Lembrete enviado para {nome_cliente}: {resultado.get('message_id')}")
            return True
        else:
            print(f"❌ Erro ao enviar lembrete: {resultado.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao enviar lembrete individual: {e}")
        return False
        
    finally:
        if cursor:
            cursor.close()
        conn.close()

if __name__ == "__main__":
    """
    Execução direta para testes
    """
    import sys
    
    if len(sys.argv) > 1:
        # Envio individual: python lembretes_whatsapp.py 123
        agendamento_id = int(sys.argv[1])
        print(f"📱 Enviando lembrete para agendamento {agendamento_id}...")
        enviar_lembrete_individual(agendamento_id)
    else:
        # Envio em lote: python lembretes_whatsapp.py
        print("📱 Enviando lembretes diários...")
        enviar_lembretes_diarios()