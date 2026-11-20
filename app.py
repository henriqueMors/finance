import yfinance as yf
import streamlit as st

st.title("Financial Data App")
st.header("Informações Financeiras de Ações")

#BBDC3.SA
#ENBR3.SA
#MULT3.SA
#BBAS3.SA
#CCRO3.SA
#LREN3.SA
#ITSA4.SA
#BBDC4.SA
#CMIG4.SA
#UGPA3.SA
#ECOR3.SA
#KLBN11.SA
#JBSS3.SA
#OIBR4.SA
#SBSP3.SA
#USIM5.SA
#VALE5.SA
#PCAR4.SA

tickerSimbolo = st.text_input(
    "Digite o símbolo da ação (ex: BBDC3.SA):", "BBDC3.SA"
    )

tickerData = yf.Ticker(tickerSimbolo)

tickerDF = tickerData.history(
    period="1d", 
    start="2020-01-01", 
    end="2024-12-31"
    )

st.header("Gráfico de fechamento")

st.line_chart(tickerDF.Close)

st.header("Gráfico de volume")

st.line_chart(tickerDF.Volume)