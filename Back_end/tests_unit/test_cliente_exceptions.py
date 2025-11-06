import pytest
from unittest.mock import patch, MagicMock
from Back_end import cliente

def test_cadastrar_cliente_exception():
    with patch('Back_end.cliente.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            cliente.cadastrar_cliente('Nome', '11999999999', 'Masculino', '1990-01-01', 'email@x.com', 'Senha!1')

def test_verificar_login_exception():
    with patch('Back_end.cliente.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            cliente.verificar_login('email@x.com', 'Senha!1')

def test_cadastrar_agendamento_exception():
    with patch('Back_end.cliente.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            cliente.cadastrar_agendamento(1, 2, '2025-11-10T10:00')

def test_atualizar_conta_exception():
    with patch('Back_end.cliente.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            cliente.atualizar_conta(1, 'Nome', '11999999999', 'email@x.com')

def test_excluir_cliente_exception():
    with patch('Back_end.cliente.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            cliente.excluir_cliente(1)
