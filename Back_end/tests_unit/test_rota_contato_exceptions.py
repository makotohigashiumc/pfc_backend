import pytest
from unittest.mock import patch, MagicMock
from Back_end import rota_contato

def test_enviar_mensagem_contato_exception():
    from Back_end import app
    with app.app.app_context():
        with patch('Back_end.email_api.send_email', side_effect=Exception('Email error')):
            result = rota_contato.enviar_mensagem_contato()
            assert result is not None
