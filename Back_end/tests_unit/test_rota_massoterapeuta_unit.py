import pytest
from unittest.mock import patch, MagicMock
from Back_end import rota_massoterapeuta

@patch('Back_end.rota_massoterapeuta.login_massoterapeuta')
def test_login_massoterapeuta(mock_func):
    mock_func.return_value = {'token': 'abc'}
    result = rota_massoterapeuta.login_massoterapeuta()
    assert 'token' in result

@patch('Back_end.rota_massoterapeuta.get_massoterapeutas')
def test_get_massoterapeutas(mock_func):
    mock_func.return_value = [{'id': 1}]
    result = rota_massoterapeuta.get_massoterapeutas()
    assert isinstance(result, list)

@patch('Back_end.rota_massoterapeuta.get_clientes')
def test_get_clientes(mock_func):
    mock_func.return_value = [{'id': 1}]
    result = rota_massoterapeuta.get_clientes()
    assert isinstance(result, list)

@patch('Back_end.rota_massoterapeuta.get_agendamentos_pendentes')
def test_get_agendamentos_pendentes(mock_func):
    mock_func.return_value = [{'id': 1}]
    result = rota_massoterapeuta.get_agendamentos_pendentes()
    assert isinstance(result, list)

@patch('Back_end.rota_massoterapeuta.get_agendamentos_confirmados')
def test_get_agendamentos_confirmados(mock_func):
    mock_func.return_value = [{'id': 1}]
    result = rota_massoterapeuta.get_agendamentos_confirmados()
    assert isinstance(result, list)

@patch('Back_end.rota_massoterapeuta.get_agendamentos')
def test_get_agendamentos(mock_func):
    mock_func.return_value = [{'id': 1}]
    result = rota_massoterapeuta.get_agendamentos()
    assert isinstance(result, list)

@patch('Back_end.rota_massoterapeuta.buscar_paciente')
def test_buscar_paciente(mock_func):
    mock_func.return_value = {'id': 1}
    result = rota_massoterapeuta.buscar_paciente()
    assert 'id' in result

@patch('Back_end.rota_massoterapeuta.atualizar_perfil')
def test_atualizar_perfil(mock_func):
    mock_func.return_value = {'status': 'updated'}
    result = rota_massoterapeuta.atualizar_perfil()
    assert result['status'] == 'updated'

@patch('Back_end.rota_massoterapeuta.atualizar_status_agendamento')
def test_atualizar_status_agendamento(mock_func):
    mock_func.return_value = {'status': 'ok'}
    result = rota_massoterapeuta.atualizar_status_agendamento(1)
    assert result['status'] == 'ok'

@patch('Back_end.rota_massoterapeuta.cancelar_agendamento_com_notificacao')
def test_cancelar_agendamento_com_notificacao(mock_func):
    mock_func.return_value = {'status': 'cancelled'}
    result = rota_massoterapeuta.cancelar_agendamento_com_notificacao(1)
    assert result['status'] == 'cancelled'

@patch('Back_end.rota_massoterapeuta.excluir_cliente_por_massoterapeuta')
def test_excluir_cliente_por_massoterapeuta(mock_func):
    mock_func.return_value = {'status': 'deleted'}
    result = rota_massoterapeuta.excluir_cliente_por_massoterapeuta(1)
    assert result['status'] == 'deleted'
