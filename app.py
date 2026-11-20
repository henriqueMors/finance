import yfinance as yf
import streamlit as st

# Busca a cotação atual e a do dia anterior (para mostrar a variação)
@st.cache_data(ttl=600)  # guarda por 10 minutos, para não consultar a cada clique
def cotacao(codigo):
    historico = yf.Ticker(codigo).history(period="5d")
    if len(historico) < 2:
        return None, None
    atual = historico["Close"].iloc[-1]
    anterior = historico["Close"].iloc[-2]
    return atual, atual - anterior


# Monta uma faixa rolante (carrossel) com as cotações de uma lista de itens
# itens: lista de (nome, código, prefixo) | duracao: segundos de uma volta completa
def faixa_cotacoes(itens, duracao=20):
    blocos = ""
    for nome, codigo, prefixo in itens:
        valor, variacao = cotacao(codigo)
        if valor is None:
            blocos += f'<span class="item"><b>{nome}</b> indisponível</span>'
            continue
        cor = "#21c354" if variacao >= 0 else "#ff4b4b"
        seta = "▲" if variacao >= 0 else "▼"
        blocos += (
            f'<span class="item"><b>{nome}</b> {prefixo} {valor:.2f} '
            f'<span style="color:{cor}">{seta} {variacao:+.2f}</span></span>'
        )

    st.html(f"""
    <style>
    .faixa {{ overflow: hidden; white-space: nowrap; padding: 8px 0;
              border-top: 1px solid rgba(128,128,128,.3);
              border-bottom: 1px solid rgba(128,128,128,.3); }}
    .trilho {{ display: inline-block; animation: rolar linear infinite; }}
    .faixa:hover .trilho {{ animation-play-state: paused; }}
    .item {{ margin: 0 40px; font-size: 1.05rem; }}
    @keyframes rolar {{ from {{ transform: translateX(0); }}
                        to   {{ transform: translateX(-50%); }} }}
    </style>
    <div class="faixa">
        <div class="trilho" style="animation-duration: {duracao}s;">{blocos}{blocos}</div>
    </div>
    """)


# ---- Listas ----
moedas = [
    ("Dólar (US$ 1)", "USDBRL=X", "R$"),
    ("Euro (€ 1)", "EURBRL=X", "R$"),
    ("Real (R$ 1)", "BRLUSD=X", "US$"),
]

ativos = (
    "BBAS3.SA",   # Banco do Brasil
    "BBDC3.SA",   # Bradesco ON
    "BBDC4.SA",   # Bradesco PN
    "ITUB4.SA",   # Itaú Unibanco
    "ITSA4.SA",   # Itaúsa
    "B3SA3.SA",   # B3
    "PETR4.SA",   # Petrobras
    "VALE3.SA",   # Vale (no lugar da VALE5)
    "ABEV3.SA",   # Ambev
    "WEGE3.SA",   # WEG
    "SUZB3.SA",   # Suzano
    "KLBN11.SA",  # Klabin
    "USIM5.SA",   # Usiminas
    "CMIG4.SA",   # Cemig
    "SBSP3.SA",   # Sabesp
    "UGPA3.SA",   # Ultrapar
    "MULT3.SA",   # Multiplan
    "LREN3.SA",   # Lojas Renner
    "PCAR3.SA",   # Pão de Açúcar (no lugar da PCAR4)
    "MOTV3.SA",   # Motiva, antiga CCR (no lugar da CCRO3)
)

# Transforma os códigos no formato da faixa: ("BBAS3", "BBAS3.SA", "R$")
itens_acoes = [(codigo.replace(".SA", ""), codigo, "R$") for codigo in ativos]

# ---- Carrosséis no topo da página ----
faixa_cotacoes(moedas, duracao=20)
faixa_cotacoes(itens_acoes, duracao=90)

# ---- Título ----
st.title("Financial Data App", text_alignment="center")
st.header("Informações Financeiras de Ações", text_alignment="center")

# ---- Escolha do ativo ----
tickerSimbolo = st.selectbox(
    "Selecione ou digite o ativo:",
    ativos,
    index=1,
    accept_new_options=True
)

# Acrescenta o .SA automaticamente, se o usuário não digitar
simbolo = tickerSimbolo.strip().upper()
if not simbolo.endswith(".SA"):
    simbolo = simbolo + ".SA"

# ---- Dados e gráficos ----
tickerData = yf.Ticker(simbolo)

tickerDF = tickerData.history(
    start="2020-01-01",
    end="2024-12-31"
)

if tickerDF.empty:
    st.warning(f"Nenhum dado encontrado para {simbolo}. Confira se o código está correto.")
else:
    st.header("Gráfico de fechamento")
    st.line_chart(tickerDF.Close)

    st.header("Gráfico de volume")
    st.line_chart(tickerDF.Volume)

    st.header("Gráfico de dividendos")
    dividendos = tickerDF.Dividends[tickerDF.Dividends > 0]

    if dividendos.empty:
        st.info("Esta ação não pagou dividendos no período.")
    else:
        st.bar_chart(dividendos)