import pandas as pd
import pytest

from calculos import indicadores, formatar_moeda, formatar_volume


@pytest.fixture
def tabela():
    datas = pd.to_datetime(["2023-01-02", "2023-06-01", "2024-01-02", "2024-06-03", "2024-12-30"])
    return pd.DataFrame({
        "Close": [10.0, 8.0, 12.0, 15.0, 12.5],
        "Volume": [100, 200, 300, 400, 500],
        "Dividends": [0.0, 0.5, 0.0, 0.3, 0.2],
    }, index=datas)


def test_indicadores(tabela):
    d = indicadores(tabela)
    assert d["ultimo_fechamento"] == 12.5
    assert d["variacao_dia"] == pytest.approx(-2.5)
    assert d["variacao_periodo_pct"] == pytest.approx(25.0)   # 10 -> 12,5
    assert d["maxima"] == 15.0 and d["minima"] == 8.0
    assert d["volume_medio"] == 300
    assert d["dividendos_total"] == pytest.approx(1.0)
    assert d["dividendos_12m"] == pytest.approx(0.5)          # só 2024
    assert d["dividend_yield_pct"] == pytest.approx(4.0)      # 0,5 / 12,5


@pytest.mark.parametrize("valor, esperado", [
    (1234.5, "R$ 1.234,50"),
    (0.2, "R$ 0,20"),
])
def test_formatar_moeda(valor, esperado):
    assert formatar_moeda(valor) == esperado


@pytest.mark.parametrize("valor, esperado", [
    (12_345_678, "12,3 mi"),
    (2_500_000_000, "2,5 bi"),
    (4_500, "4,5 mil"),
    (80, "80"),
])
def test_formatar_volume(valor, esperado):
    assert formatar_volume(valor) == esperado
