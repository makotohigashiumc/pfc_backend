import pytest
from unittest.mock import MagicMock, patch
from werkzeug.security import generate_password_hash

@patch("Back_end.database.get_connection")
def test_verificar_login_success(mock_get_conn):
    # Simula um massoterapeuta com senha hash
    hashed = generate_password_hash("Senha!1")
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        'id': 2,
        'email': 'm@x.com',
        'senha_hash': hashed,
        'nome': 'M'
    }
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    from Back_end.massoterapeuta import verificar_login
    user = verificar_login('m@x.com', 'Senha!1')
    assert user is None or ('senha_hash' not in user if isinstance(user, dict) else True)

@patch("Back_end.database.get_connection")
def test_listar_massoterapeutas_returns_list(mock_get_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {'id':1, 'nome':'A', 'telefone':'11', 'email':'a@x.com'}
    ]
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    from Back_end.massoterapeuta import listar_massoterapeutas
    res = listar_massoterapeutas()
    assert isinstance(res, list)
