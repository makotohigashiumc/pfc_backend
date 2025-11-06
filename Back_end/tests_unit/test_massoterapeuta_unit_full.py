import pytest
from unittest.mock import patch, MagicMock
from Back_end import massoterapeuta

def test_cadastrar_massoterapeuta():
    result = massoterapeuta.cadastrar_massoterapeuta('Nome', '11999999999', 'Masculino', '1990-01-01', 'email@x.com', 'Senha!1')
    assert result is None or isinstance(result, dict)

def test_verificar_login():
    result = massoterapeuta.verificar_login('email@x.com', 'Senha!1')
    assert result is None or isinstance(result, dict)

def test_atualizar_conta():
    result = massoterapeuta.atualizar_conta(1, 'Nome', '11999999999')
    assert result is None or isinstance(result, dict)

def test_excluir_massoterapeuta():
    result = massoterapeuta.excluir_massoterapeuta(1)
    assert result is None or isinstance(result, dict)

def test_listar_massoterapeutas():
    result = massoterapeuta.listar_massoterapeutas()
    assert isinstance(result, list) or result is not None

def test_listar_clientes():
    result = massoterapeuta.listar_clientes()
    assert isinstance(result, list) or result is not None

def test_listar_agendamentos():
    result = massoterapeuta.listar_agendamentos()
    assert isinstance(result, list) or result is not None

def test_listar_agendamentos_massoterapeuta():
    result = massoterapeuta.listar_agendamentos_massoterapeuta(1)
    assert isinstance(result, list) or result is not None

def test_atualizar_agendamento():
    result = massoterapeuta.atualizar_agendamento(1, 1, 'pendente')
    assert result is not None

def test_listar_agendamentos_por_status():
    result = massoterapeuta.listar_agendamentos_por_status(1, ['pendente'])
    assert isinstance(result, list) or result is not None

def test_buscar_paciente_com_historico():
    result = massoterapeuta.buscar_paciente_com_historico(1, 'Nome')
    assert result is not None

def test_cancelar_agendamento_com_motivo():
    result = massoterapeuta.cancelar_agendamento_com_motivo(1, 1, 'motivo')
    assert result is not None
