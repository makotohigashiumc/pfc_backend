import pytest
from unittest.mock import patch, MagicMock
from Back_end import rota_massoterapeuta

def test_login_massoterapeuta_exception():
    from Back_end import app
    with app.app.test_request_context(json={"email": "email@x.com", "senha": "123"}):
        with patch('Back_end.massoterapeuta.verificar_login', side_effect=Exception('Login error')):
            result = rota_massoterapeuta.login_massoterapeuta()
            assert result is not None

def test_get_massoterapeutas_exception():
    from Back_end import app
    with app.app.test_client() as client:
        # Patch no namespace da rota, não no módulo original
        with patch('Back_end.rota_massoterapeuta.listar_massoterapeutas', side_effect=Exception('DB error')):
            response = client.get('/api/massoterapeuta/lista')
            assert response.status_code == 500
