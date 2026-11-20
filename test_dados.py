import pytest

from dados import normalizar_simbolo


@pytest.mark.parametrize("digitado, esperado", [
    ("PETR3", "PETR3.SA"),
    ("petr3", "PETR3.SA"),      # minúsculo
    ("  vale3  ", "VALE3.SA"),  # espaços
    ("BBDC3.SA", "BBDC3.SA"),   # já tem .SA
])
def test_normalizar_simbolo(digitado, esperado):
    assert normalizar_simbolo(digitado) == esperado
