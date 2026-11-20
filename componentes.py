# Partes visuais da página
import streamlit as st

from calculos import indicadores, formatar_moeda, formatar_volume
from dados import cotacao
from estilos import CSS_FAIXA, COR_ALTA, COR_BAIXA


def faixa_cotacoes(itens, duracao=20):
    """Carrossel com as cotações. itens: lista de (nome, código, prefixo)."""
    blocos = ""
    for nome, codigo, prefixo in itens:
        valor, variacao = cotacao(codigo)
        if valor is None:
            blocos += f'<span class="item"><b>{nome}</b> indisponível</span>'
            continue
        cor = COR_ALTA if variacao >= 0 else COR_BAIXA
        seta = "▲" if variacao >= 0 else "▼"
        blocos += (
            f'<span class="item"><b>{nome}</b> {prefixo} {valor:.2f} '
            f'<span style="color:{cor}">{seta} {variacao:+.2f}</span></span>'
        )

    st.html(f"""
    {CSS_FAIXA}
    <div class="faixa">
        <div class="trilho" style="animation-duration: {duracao}s;">{blocos}{blocos}</div>
    </div>
    """)


def resumo_numerico(tabela):
    """Cards com os principais números do ativo no período."""
    dados = indicadores(tabela)

    st.header("Resumo do período")

    linha1 = st.columns(4)
    linha1[0].metric(
        "Último fechamento",
        formatar_moeda(dados["ultimo_fechamento"]),
        f"{dados['variacao_dia']:+.2f} no dia",
    )
    linha1[1].metric(
        "Variação no período",
        f"{dados['variacao_periodo_pct']:+.2f}%".replace(".", ","),
    )
    linha1[2].metric(
        "Máxima",
        formatar_moeda(dados["maxima"]),
        dados["data_maxima"].strftime("em %d/%m/%Y"),
        delta_color="off",
        delta_arrow="off",
    )
    linha1[3].metric(
        "Mínima",
        formatar_moeda(dados["minima"]),
        dados["data_minima"].strftime("em %d/%m/%Y"),
        delta_color="off",
        delta_arrow="off",
    )

    linha2 = st.columns(4)
    linha2[0].metric("Volume médio diário", formatar_volume(dados["volume_medio"]))
    linha2[1].metric("Dividendos no período", formatar_moeda(dados["dividendos_total"]))
    linha2[2].metric("Dividendos 12 meses", formatar_moeda(dados["dividendos_12m"]))
    linha2[3].metric(
        "Dividend yield",
        f"{dados['dividend_yield_pct']:.2f}%".replace(".", ","),
        help="Dividendos pagos nos últimos 12 meses ÷ último preço",
    )

    st.subheader("Últimos pregões")
    recentes = tabela[["Open", "High", "Low", "Close", "Volume"]].tail(10).iloc[::-1].copy()
    recentes.index = recentes.index.strftime("%d/%m/%Y")
    recentes.columns = ["Abertura", "Máxima", "Mínima", "Fechamento", "Volume"]
    st.dataframe(
        recentes,
        column_config={
            col: st.column_config.NumberColumn(format="R$ %.2f")
            for col in ["Abertura", "Máxima", "Mínima", "Fechamento"]
        } | {"Volume": st.column_config.NumberColumn(format="localized")},
    )


def graficos_ativo(tabela, simbolo):
    """Números e gráficos de fechamento, volume e dividendos do ativo."""
    if tabela.empty:
        st.warning(f"Nenhum dado encontrado para {simbolo}. Confira se o código está correto.")
        return

    resumo_numerico(tabela)

    st.header("Gráfico de fechamento")
    st.line_chart(tabela.Close)

    st.header("Gráfico de volume")
    st.line_chart(tabela.Volume)

    st.header("Gráfico de dividendos")
    dividendos = tabela.Dividends[tabela.Dividends > 0]
    if dividendos.empty:
        st.info("Esta ação não pagou dividendos no período.")
    else:
        st.bar_chart(dividendos)
