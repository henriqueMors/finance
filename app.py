import streamlit as st

from ativos import MOEDAS, ATIVOS, ITENS_ACOES, DATA_INICIO, DATA_FIM
from dados import normalizar_simbolo, historico_ativo
from componentes import faixa_cotacoes, graficos_ativo

# Carrosséis no topo
faixa_cotacoes(MOEDAS, duracao=20)
faixa_cotacoes(ITENS_ACOES, duracao=90)

# Título
st.title("Financial Data App", text_alignment="center")
st.header("Informações Financeiras de Ações", text_alignment="center")

# Escolha do ativo
escolha = st.selectbox(
    "Selecione ou digite o ativo:", ATIVOS, index=1, accept_new_options=True
)
simbolo = normalizar_simbolo(escolha)

# Gráficos
tabela = historico_ativo(simbolo, DATA_INICIO, DATA_FIM)
graficos_ativo(tabela, simbolo)
