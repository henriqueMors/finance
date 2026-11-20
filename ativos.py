# Listas de moedas e ações usadas no app (só dados, sem lógica)

# (nome exibido, código no Yahoo Finance, prefixo do valor)
MOEDAS = [
    ("Dólar (US$ 1)", "USDBRL=X", "R$"),
    ("Euro (€ 1)", "EURBRL=X", "R$"),
    ("Real (R$ 1)", "BRLUSD=X", "US$"),
]

ATIVOS = (
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

# Ações no formato da faixa: ("BBAS3", "BBAS3.SA", "R$")
ITENS_ACOES = [(codigo.replace(".SA", ""), codigo, "R$") for codigo in ATIVOS]

# Período dos gráficos
DATA_INICIO = "2020-01-01"
DATA_FIM = "2024-12-31"
