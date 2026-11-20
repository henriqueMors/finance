# Partes visuais da página
import streamlit as st

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


def graficos_ativo(tabela, simbolo):
    """Gráficos de fechamento, volume e dividendos do ativo."""
    if tabela.empty:
        st.warning(f"Nenhum dado encontrado para {simbolo}. Confira se o código está correto.")
        return

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
