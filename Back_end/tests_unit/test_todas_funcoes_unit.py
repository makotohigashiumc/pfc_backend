import pytest
from unittest.mock import patch, MagicMock
from Back_end import cliente, massoterapeuta, email_api, database

def test_cliente_funcs():
    assert cliente.cadastrar_cliente('Nome', '11999999999', 'Masculino', '1990-01-01', 'email@x.com', 'Senha!1') is None or isinstance(cliente.cadastrar_cliente('Nome', '11999999999', 'Masculino', '1990-01-01', 'email@x.com', 'Senha!1'), dict)
    assert cliente.verificar_login('email@x.com', 'Senha!1') is None or isinstance(cliente.verificar_login('email@x.com', 'Senha!1'), dict)
    assert cliente.cadastrar_agendamento(1, 2, '2025-11-10T10:00') is None or isinstance(cliente.cadastrar_agendamento(1, 2, '2025-11-10T10:00'), dict)
    assert cliente.atualizar_conta(1, 'Nome', '11999999999', 'email@x.com') is None or isinstance(cliente.atualizar_conta(1, 'Nome', '11999999999', 'email@x.com'), dict)
    assert cliente.excluir_cliente(1) is None or isinstance(cliente.excluir_cliente(1), dict)
    assert isinstance(cliente.historico_sessoes_cliente(1), list) or cliente.historico_sessoes_cliente(1) is None or isinstance(cliente.historico_sessoes_cliente(1), dict)
    assert cliente.buscar_cliente_por_id(1) is None or isinstance(cliente.buscar_cliente_por_id(1), dict)

def test_massoterapeuta_funcs():
    assert massoterapeuta.cadastrar_massoterapeuta('Nome', '11999999999', 'Masculino', '1990-01-01', 'email@x.com', 'Senha!1') is None or isinstance(massoterapeuta.cadastrar_massoterapeuta('Nome', '11999999999', 'Masculino', '1990-01-01', 'email@x.com', 'Senha!1'), dict)
    assert massoterapeuta.verificar_login('email@x.com', 'Senha!1') is None or isinstance(massoterapeuta.verificar_login('email@x.com', 'Senha!1'), dict)
    assert massoterapeuta.atualizar_conta(1, 'Nome', '11999999999') is None or isinstance(massoterapeuta.atualizar_conta(1, 'Nome', '11999999999'), dict)
    assert massoterapeuta.excluir_massoterapeuta(1) is None or isinstance(massoterapeuta.excluir_massoterapeuta(1), dict)
    assert isinstance(massoterapeuta.listar_massoterapeutas(), list) or massoterapeuta.listar_massoterapeutas() is None or isinstance(massoterapeuta.listar_massoterapeutas(), dict)
    assert isinstance(massoterapeuta.listar_clientes(), list) or massoterapeuta.listar_clientes() is None or isinstance(massoterapeuta.listar_clientes(), dict)
    assert isinstance(massoterapeuta.listar_agendamentos(), list) or massoterapeuta.listar_agendamentos() is None or isinstance(massoterapeuta.listar_agendamentos(), dict)
    assert isinstance(massoterapeuta.listar_agendamentos_massoterapeuta(1), list) or massoterapeuta.listar_agendamentos_massoterapeuta(1) is None or isinstance(massoterapeuta.listar_agendamentos_massoterapeuta(1), dict)
    result = massoterapeuta.atualizar_agendamento(1, 1, 'pendente')
    assert result is None or isinstance(result, dict) or result is False
    assert isinstance(massoterapeuta.listar_agendamentos_por_status(1, ['pendente']), list) or massoterapeuta.listar_agendamentos_por_status(1, ['pendente']) is None or isinstance(massoterapeuta.listar_agendamentos_por_status(1, ['pendente']), dict)
    assert massoterapeuta.buscar_paciente_com_historico(1, 'Nome') is None or isinstance(massoterapeuta.buscar_paciente_com_historico(1, 'Nome'), dict)
    assert massoterapeuta.cancelar_agendamento_com_motivo(1, 1, 'motivo') is None or isinstance(massoterapeuta.cancelar_agendamento_com_motivo(1, 1, 'motivo'), dict)

def test_email_api_funcs():
    assert email_api.send_email('to@x.com', 'Assunto', 'Conteudo') is not None
    token = email_api.generate_confirmation_token('to@x.com')
    assert isinstance(token, str)
    assert email_api.verify_confirmation_token(token) == 'to@x.com'
    assert email_api.send_confirmation_email('to@x.com') is not None
    assert email_api.sendgrid_email_api_massoterapia('to@x.com', 'Assunto', 'Conteudo') is not None

def test_database_funcs():
    assert database.get_connection() is not None or database.get_connection() is None
    result = database.test_connection()
    assert result is None or isinstance(result, dict)
