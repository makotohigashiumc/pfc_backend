import pytest
from unittest.mock import patch, MagicMock
from Back_end import massoterapeuta

def test_cadastrar_massoterapeuta_exception():
    with patch('Back_end.massoterapeuta.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            massoterapeuta.cadastrar_massoterapeuta('Nome', '11999999999', 'Masculino', '1990-01-01', 'email@x.com', 'Senha!1')

def test_verificar_login_exception():
    with patch('Back_end.massoterapeuta.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            massoterapeuta.verificar_login('email@x.com', 'Senha!1')

def test_atualizar_conta_exception():
    with patch('Back_end.massoterapeuta.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            massoterapeuta.atualizar_conta(1, 'Nome', '11999999999')

def test_excluir_massoterapeuta_exception():
    with patch('Back_end.massoterapeuta.get_connection', side_effect=Exception('DB error')):
        with pytest.raises(Exception):
            massoterapeuta.excluir_massoterapeuta(1)
