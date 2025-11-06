import pytest
from unittest.mock import patch, MagicMock
from Back_end import rota_clientes

@patch('Back_end.rota_clientes.confirmar_email')
def test_confirmar_email(mock_confirmar_email):
    mock_confirmar_email.return_value = True
    token = 'fake-token'
    result = rota_clientes.confirmar_email(token)
    assert result is True

@patch('Back_end.rota_clientes.recuperar_senha')
def test_recuperar_senha(mock_recuperar_senha):
    mock_recuperar_senha.return_value = {'status': 'ok'}
    result = rota_clientes.recuperar_senha()
    assert result['status'] == 'ok'

@patch('Back_end.rota_clientes.redefinir_senha')
def test_redefinir_senha(mock_redefinir_senha):
    mock_redefinir_senha.return_value = {'status': 'ok'}
    result = rota_clientes.redefinir_senha()
    assert result['status'] == 'ok'

@patch('Back_end.rota_clientes.api_cadastrar_cliente')
def test_api_cadastrar_cliente(mock_api_cadastrar_cliente):
    mock_api_cadastrar_cliente.return_value = {'id': 1}
    result = rota_clientes.api_cadastrar_cliente()
    assert 'id' in result

@patch('Back_end.rota_clientes.api_login')
def test_api_login(mock_api_login):
    mock_api_login.return_value = {'token': 'abc'}
    result = rota_clientes.api_login()
    assert 'token' in result

@patch('Back_end.rota_clientes.api_cadastrar_agendamento')
def test_api_cadastrar_agendamento(mock_api_cadastrar_agendamento):
    mock_api_cadastrar_agendamento.return_value = {'id': 1}
    result = rota_clientes.api_cadastrar_agendamento()
    assert 'id' in result

@patch('Back_end.rota_clientes.api_historico_agendamentos')
def test_api_historico_agendamentos(mock_api_historico_agendamentos):
    mock_api_historico_agendamentos.return_value = []
    result = rota_clientes.api_historico_agendamentos()
    assert isinstance(result, list)

@patch('Back_end.rota_clientes.api_atualizar_cliente')
def test_api_atualizar_cliente(mock_api_atualizar_cliente):
    mock_api_atualizar_cliente.return_value = {'status': 'updated'}
    result = rota_clientes.api_atualizar_cliente()
    assert result['status'] == 'updated'

@patch('Back_end.rota_clientes.api_excluir_cliente')
def test_api_excluir_cliente(mock_api_excluir_cliente):
    mock_api_excluir_cliente.return_value = {'status': 'deleted'}
    result = rota_clientes.api_excluir_cliente()
    assert result['status'] == 'deleted'

@patch('Back_end.rota_clientes.api_me')
def test_api_me(mock_api_me):
    mock_api_me.return_value = {'id': 1}
    result = rota_clientes.api_me()
    assert 'id' in result

@patch('Back_end.rota_clientes.horarios_ocupados_massoterapeuta')
def test_horarios_ocupados_massoterapeuta(mock_func):
    mock_func.return_value = ['10:00', '11:00']
    result = rota_clientes.horarios_ocupados_massoterapeuta(1)
    assert '10:00' in result

@patch('Back_end.rota_clientes.cancelar_agendamento_cliente')
def test_cancelar_agendamento_cliente(mock_func):
    mock_func.return_value = {'status': 'cancelled'}
    result = rota_clientes.cancelar_agendamento_cliente(1)
    assert result['status'] == 'cancelled'

@patch('Back_end.rota_clientes.limpar_historico_agendamentos')
def test_limpar_historico_agendamentos(mock_func):
    mock_func.return_value = {'status': 'ok'}
    result = rota_clientes.limpar_historico_agendamentos()
    assert result['status'] == 'ok'
