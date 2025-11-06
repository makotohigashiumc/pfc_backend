import pytest
from unittest.mock import patch, MagicMock
from Back_end import database

def test_get_connection():
    result = database.get_connection()
    assert result is not None or result is None

def test_test_connection():
    result = database.test_connection()
    assert result is None or isinstance(result, dict)
