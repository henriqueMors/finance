# Busca e preparo dos dados (Yahoo Finance)
import pandas as pd
import streamlit as st
import yfinance as yf


def normalizar_simbolo(texto):
    """'petr3 ' -> 'PETR3.SA'. Acrescenta o .SA se o usuário não digitar."""
    simbolo = texto.strip().upper()
    if not simbolo.endswith(".SA"):
        simbolo = simbolo + ".SA"
    return simbolo


# ---- Consultas ao Yahoo (com cache de 10 minutos) ----
# Se a consulta falhar, o erro NÃO fica no cache: na próxima vez ele tenta de novo.

@st.cache_data(ttl=600)
def _buscar_cotacao(codigo):
    historico = yf.Ticker(codigo).history(period="5d")
    if len(historico) < 2:
        return None, None
    atual = historico["Close"].iloc[-1]
    anterior = historico["Close"].iloc[-2]
    return atual, atual - anterior


@st.cache_data(ttl=600)
def _buscar_historico(simbolo, inicio, fim):
    return yf.Ticker(simbolo).history(start=inicio, end=fim)


# ---- Funções usadas pelo app (nunca derrubam a página) ----

def cotacao(codigo):
    """Devolve (valor atual, variação desde o fechamento anterior) ou (None, None)."""
    try:
        return _buscar_cotacao(codigo)
    except Exception:
        return None, None  # sem internet, Yahoo fora do ar etc.


def historico_ativo(simbolo, inicio, fim):
    """Tabela com fechamento, volume e dividendos do ativo no período (vazia se falhar)."""
    try:
        return _buscar_historico(simbolo, inicio, fim)
    except Exception:
        return pd.DataFrame()
