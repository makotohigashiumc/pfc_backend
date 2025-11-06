import pytest
from unittest.mock import patch, MagicMock
from Back_end import email_api

def test_send_email():
    result = email_api.send_email('to@x.com', 'Assunto', 'Conteudo')
    assert result is not None

def test_generate_confirmation_token():
    token = email_api.generate_confirmation_token('to@x.com')
    assert isinstance(token, str)

def test_verify_confirmation_token():
    email = 'to@x.com'
    token = email_api.generate_confirmation_token(email)
    decoded = email_api.verify_confirmation_token(token)
    assert decoded == email

def test_send_confirmation_email():
    result = email_api.send_confirmation_email('to@x.com')
    assert result is not None

def test_sendgrid_email_api_massoterapia():
    result = email_api.sendgrid_email_api_massoterapia('to@x.com', 'Assunto', 'Conteudo')
    assert result is not None
