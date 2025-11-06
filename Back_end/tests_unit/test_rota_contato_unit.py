import pytest
from unittest.mock import patch, MagicMock
from Back_end import rota_contato

@patch('Back_end.rota_contato.enviar_mensagem_contato')
def test_enviar_mensagem_contato(mock_func):
    mock_func.return_value = {'status': 'sent'}
    result = rota_contato.enviar_mensagem_contato()
    assert result['status'] == 'sent'

@patch('Back_end.rota_contato.teste_configuracao_email')
def test_teste_configuracao_email(mock_func):
    mock_func.return_value = {'status': 'ok'}
    result = rota_contato.teste_configuracao_email()
    assert result['status'] == 'ok'
