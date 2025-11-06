import pytest
from unittest.mock import patch, MagicMock
from Back_end import app

def test_index():
    with app.app.app_context():
        result = app.index()
        assert result is not None

def test_handle_422():
    err = Exception('Erro')
    with app.app.app_context():
        result = app.handle_422(err)
        assert result is not None

def test_handle_no_auth():
    err = Exception('Sem auth')
    with app.app.app_context():
        result = app.handle_no_auth(err)
        assert result is not None

def test_health_check():
    with app.app.app_context():
        result = app.health_check()
        assert result is not None
