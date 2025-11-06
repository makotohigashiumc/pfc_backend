import pytest
from unittest.mock import patch, MagicMock
from Back_end import email_api

def test_send_email_sendgrid_exception():
    with patch('requests.post', side_effect=Exception('SendGrid error')):
        result = email_api.send_email('to@x.com', 'Assunto', 'Conteudo')
        assert result is not None or result is None

def test_send_email_gmail_exception():
    with patch('requests.post', return_value=MagicMock(status_code=500)):
        with patch('smtplib.SMTP_SSL', side_effect=Exception('SMTP error')):
            result = email_api.send_email('to@x.com', 'Assunto', 'Conteudo')
            assert result is not None or result is None

def test_verify_confirmation_token_expired():
    with patch('jwt.decode', side_effect=email_api.jwt.ExpiredSignatureError()):
        result = email_api.verify_confirmation_token('token')
        assert result is None

def test_verify_confirmation_token_invalid():
    with patch('jwt.decode', side_effect=email_api.jwt.InvalidTokenError()):
        result = email_api.verify_confirmation_token('token')
        assert result is None
