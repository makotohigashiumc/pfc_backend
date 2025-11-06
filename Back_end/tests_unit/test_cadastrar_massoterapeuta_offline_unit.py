import pytest
from unittest.mock import patch, MagicMock
from Back_end import cadastrar_massoterapeuta_offline

def test_main():
    # Mockar input para evitar erro de stdin
    import builtins
    original_input = builtins.input
    builtins.input = lambda prompt='': 'Diogo'
    try:
        cadastrar_massoterapeuta_offline.main()
    except Exception:
        pytest.fail('main() levantou exceção')
    finally:
        builtins.input = original_input
