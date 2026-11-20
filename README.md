# Financial Data App

Painel web feito em **Python** com **Streamlit** para acompanhar ações da bolsa brasileira (B3) e as cotações do dólar, euro e real. Os dados vêm do **Yahoo Finance**, por meio da biblioteca `yfinance`.

## Funcionalidades

- **Carrossel de moedas** no topo da página: dólar, euro e real, com a variação desde o fechamento anterior (▲ verde para alta, ▼ vermelho para baixa)
- **Carrossel de ações** com a cotação e a variação dos ativos da lista
- O carrossel **pausa ao passar o mouse**, para facilitar a leitura
- **Seleção do ativo** por lista, com a opção de **digitar qualquer outro código** (ex.: `PETR3`)
- O sufixo `.SA` é acrescentado automaticamente (`petr3` → `PETR3.SA`)
- **Resumo numérico** do ativo escolhido:
  - último fechamento e variação no dia
  - variação no período (%)
  - máxima e mínima, com as datas
  - volume médio diário
  - dividendos no período e nos últimos 12 meses
  - dividend yield (dividendos dos últimos 12 meses ÷ último preço)
  - tabela com os **últimos 10 pregões** (abertura, máxima, mínima, fechamento e volume)
- Gráficos do ativo escolhido:
  - **Fechamento** (preço ao fim de cada dia)
  - **Volume** negociado
  - **Dividendos** pagos por ação (somente as datas com pagamento)
- **Cache de 10 minutos**: os dados não são consultados novamente a cada clique, o que deixa o app mais rápido
- **Tolerante a falhas**: se o Yahoo Finance não responder, o app mostra "indisponível" e um aviso, sem derrubar a página
- Compatível com os temas **claro** e **escuro**

## Estrutura do projeto

```
financial_app/
├── app.py          # monta a página e organiza os componentes
├── ativos.py       # listas de moedas e ações e período dos gráficos
├── dados.py        # consultas ao Yahoo Finance, cache e tratamento do código do ativo
├── calculos.py     # indicadores numéricos e formatação (R$, volume)
├── componentes.py  # carrossel, resumo numérico e gráficos
├── estilos.py      # CSS do carrossel e cores de alta/baixa
├── test_dados.py   # testes do tratamento do código do ativo
└── test_calculos.py # testes dos indicadores e da formatação
```

Cada arquivo tem uma responsabilidade:

| Para... | altere |
|---|---|
| incluir ou remover ações e moedas | `ativos.py` |
| mudar o período dos gráficos | `ativos.py` (`DATA_INICIO` e `DATA_FIM`) |
| trocar a fonte de dados | `dados.py` |
| criar ou mudar um indicador numérico | `calculos.py` |
| mudar cores, velocidade ou aparência | `estilos.py` e `componentes.py` |

## Como executar

```bash
# criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# instalar as dependências
pip install streamlit yfinance pandas pytest

# rodar o app
streamlit run app.py
```

O app abre no navegador em `http://localhost:8501`.

> Na primeira abertura, o carregamento pode levar alguns segundos, porque o app consulta todas as cotações. Depois disso, o cache deixa a navegação rápida.

## Testes

```bash
pytest
```

Os testes conferem:

- o tratamento do código digitado pelo usuário (letras minúsculas, espaços, presença ou ausência do `.SA`);
- o cálculo dos indicadores (variação, máxima, mínima, dividendos, dividend yield);
- a formatação no padrão brasileiro (`R$ 1.234,50`, `12,3 mi`).

## Tecnologias

- Python 3
- Streamlit
- yfinance
- pandas
- pytest

## Observações

- Os dados do Yahoo Finance podem ter **atraso** e, com o cache, ficam até 10 minutos sem atualizar. O app é indicado para **estudo e acompanhamento**, não para operar em tempo real.
- Alguns códigos de ações mudam com o tempo (fusões, mudanças de nome, saída da bolsa). Se um ativo aparecer como "indisponível", confira se o código ainda é válido no site da B3.
- O `yfinance` não é uma API oficial do Yahoo. Se os dados pararem de carregar, atualize a biblioteca com `pip install -U yfinance`.

---

> Este projeto tem fins educacionais e não constitui recomendação de investimento.
