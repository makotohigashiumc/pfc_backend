import pytest
from unittest.mock import patch, MagicMock
from Back_end import rota_clientes

def test_confirmar_email_exception():
    with patch('Back_end.rota_clientes.verify_confirmation_token', return_value=None):
        result = rota_clientes.confirmar_email('token')
        assert isinstance(result, tuple) and result[1] == 400


def test_api_cadastrar_cliente_exception():
    from Back_end import app
    with app.app.test_request_context(json={"nome": "Nome", "telefone": "11999999999", "sexo": "Masculino", "data_nascimento": "1990-01-01", "email": "email@x.com", "senha": "123"}):
        with patch('Back_end.cliente.cadastrar_cliente', side_effect=Exception('DB error')):
            result = rota_clientes.api_cadastrar_cliente()
            assert result is not None
