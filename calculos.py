# Indicadores numéricos do ativo (regras puras: sem Streamlit, fáceis de testar)
import pandas as pd


def indicadores(tabela):
    """Recebe o histórico do ativo e devolve um dicionário com os indicadores."""
    fechamento = tabela["Close"]
    primeiro = fechamento.iloc[0]
    ultimo = fechamento.iloc[-1]

    # Dividendos dos últimos 12 meses do período (para o dividend yield)
    fim = tabela.index[-1]
    ultimos_12m = tabela[tabela.index > fim - pd.DateOffset(years=1)]
    dividendos_12m = ultimos_12m["Dividends"].sum()

    return {
        "ultimo_fechamento": ultimo,
        "variacao_dia": fechamento.iloc[-1] - fechamento.iloc[-2] if len(fechamento) > 1 else 0.0,
        "variacao_periodo_pct": (ultimo / primeiro - 1) * 100,
        "maxima": fechamento.max(),
        "data_maxima": fechamento.idxmax(),
        "minima": fechamento.min(),
        "data_minima": fechamento.idxmin(),
        "volume_medio": tabela["Volume"].mean(),
        "dividendos_total": tabela["Dividends"].sum(),
        "dividendos_12m": dividendos_12m,
        "dividend_yield_pct": dividendos_12m / ultimo * 100 if ultimo else 0.0,
    }


def formatar_moeda(valor):
    """1234.5 -> 'R$ 1.234,50' (padrão brasileiro)."""
    texto = f"{valor:,.2f}"                       # '1,234.50'
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def formatar_volume(valor):
    """12345678 -> '12,3 mi'."""
    for limite, sufixo in [(1e9, "bi"), (1e6, "mi"), (1e3, "mil")]:
        if valor >= limite:
            return f"{valor / limite:.1f} {sufixo}".replace(".", ",")
    return f"{valor:.0f}"
