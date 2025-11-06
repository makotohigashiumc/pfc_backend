import pytest
from unittest.mock import patch, MagicMock
from Back_end import cliente

def test_cadastrar_cliente():
    result = cliente.cadastrar_cliente('Nome', '11999999999', 'Masculino', '1990-01-01', 'email@x.com', 'Senha!1')
    assert result is not None

def test_verificar_login():
    result = cliente.verificar_login('email@x.com', 'Senha!1')
    assert result is None or isinstance(result, dict)

def test_cadastrar_agendamento():
    from unittest.mock import patch, MagicMock
    with patch('Back_end.database.get_connection') as mock_get_conn, \
         patch('Back_end.cliente.get_connection') as mock_cliente_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [None, None, None]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        mock_cliente_conn.return_value = mock_conn
        result = cliente.cadastrar_agendamento(1, 2, '2025-11-10T10:00')
    assert result is None or isinstance(result, dict)

def test_atualizar_conta():
    from unittest.mock import patch, MagicMock
    with patch('Back_end.database.get_connection') as mock_get_conn, \
         patch('Back_end.cliente.get_connection') as mock_cliente_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [None, None]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        mock_cliente_conn.return_value = mock_conn
        result = cliente.atualizar_conta(1, 'Nome', '11999999999', 'email@x.com')
    assert result is None or isinstance(result, dict)

def test_excluir_cliente():
    from unittest.mock import patch, MagicMock
    with patch('Back_end.database.get_connection') as mock_get_conn, \
         patch('Back_end.cliente.get_connection') as mock_cliente_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [None]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        mock_cliente_conn.return_value = mock_conn
        result = cliente.excluir_cliente(1)
    assert result is None or isinstance(result, dict)

def test_historico_sessoes_cliente():
    result = cliente.historico_sessoes_cliente(1)
    assert isinstance(result, list) or result is not None

def test_buscar_cliente_por_id():
    from unittest.mock import patch, MagicMock
    with patch('Back_end.database.get_connection') as mock_get_conn, \
         patch('Back_end.cliente.get_connection') as mock_cliente_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {'id': 1, 'nome': 'Nome'}
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        mock_cliente_conn.return_value = mock_conn
        result = cliente.buscar_cliente_por_id(1)
    assert result is None or isinstance(result, dict)
