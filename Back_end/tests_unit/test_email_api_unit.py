import pytest
from Back_end.email_api import generate_confirmation_token, verify_confirmation_token

def test_generate_and_verify_token():
    email = 'test@example.com'
    token = generate_confirmation_token(email)
    assert isinstance(token, str)
    decoded = verify_confirmation_token(token)
    assert decoded == email
