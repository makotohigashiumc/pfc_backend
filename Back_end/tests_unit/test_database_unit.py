import pytest
import os
from unittest.mock import patch


@patch('Back_end.database.os.getenv', return_value=None)
def test_get_connection_no_database_url(mock_getenv):
    from Back_end.database import get_connection
    res = get_connection()
    assert res is None
