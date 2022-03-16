#pip install streamlit
#pip install yfinance
#pip install plotly
#pip install pandas numpy json datetime

from tkinter import W
import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import datetime
import json
import yfinance as yf

st.set_page_config(page_title='DashCrypto', 
                   page_icon='📊',
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)

# Lendo o arquivo Json
with open('data.json', 'r') as _json:
    data_string = _json.read()

obj = json.loads(data_string)

crypto_names = obj["crypto_names"]
crypto_symbols = obj["crypto_symbols"]

#Criando o dicionário de nome e símbolo
crypto_dict = dict(zip(crypto_names, crypto_symbols))

crypto_selected = st.selectbox(label = 'Selecione sua cripto:', 
                               options = crypto_dict.keys())

#Criar variáveis de ambiente
today_date = datetime.datetime.now()
delta_date = datetime.timedelta(days=360)

#Criar duas colunas
col1, col2 = st.columns(2)

#Selecionando a data de início
with col1:

    start_date = st.date_input(label = 'Selecione a data de ínicio:', 
                               value = today_date - delta_date)

#Selecionando a data final
with col2:

    final_date = st.date_input(label = 'Selecione a data final:', 
                               value = today_date)

#Chamando o símbolo no yfinance
_symbol = crypto_dict[crypto_selected] + '-USD'

df = yf.Ticker(_symbol).history(interval='1d', 
                                start=start_date, 
                                end=final_date)

# st.title(f'Valores de {crypto_selected}')
fig = px.line(df, 
              x = df.index, 
              y = 'Close')

# st.plotly_chart(fig)

### Aula 3

st.markdown('___')
st.markdown('<h2> Simulador de aportes </h2>', unsafe_allow_html=True)

INTERVALS = {"Dia": "1d",
             "5 Dias": "5d",
             "Semana": "1wk",
             "Mês": "1mo",
             "3 Meses": "3mo"}

col1, col2 = st.columns(2)

with col1:
    interval_selected = st.selectbox(label='Selecione o intervalo de aportes:', 
                                    options=INTERVALS.keys(), index = 3)

with col2:
    investment_selected = st.number_input(label = 'Selecione o aporte:', 
                                        step = 100, value = 1000)

df_aporte = yf.Ticker(_symbol).history(start=start_date, 
                                       end=final_date, 
                                       interval=INTERVALS[interval_selected])['Close']
usd = yf.Ticker('BRL=X').history(start=start_date, 
                                 end=final_date, 
                                 interval=INTERVALS[interval_selected])['Close']

df_aporte = pd.DataFrame(df_aporte * usd)

df_aporte['Aporte'] = round(investment_selected, 2)
df_aporte['Aporte'][0] = 0

for i in range(len(df_aporte)-1):
    pct_change_variable = df_aporte['Close'][df_aporte.index[i]:].pct_change() + 1
    df_aporte[f'investimento_{i}'] = pct_change_variable.cumprod() * df_aporte['Aporte']
    
investimento_colunas = [f'investimento_{i}' for i in range(len(df_aporte)-1)]

df_aportes_acumulados = df_aporte[investimento_colunas].transpose()

df_resultado = pd.DataFrame()
df_resultado[f'{crypto_selected} Acum.'] = df_aportes_acumulados.sum()
df_resultado['Aporte Acum.'] = df_aporte['Aporte'].cumsum()

result = px.line(df_resultado)
result.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    margin=dict(t=10,l=10,b=10,r=10)
)

### AULA 4


valor_final_invest = df_resultado[f'{crypto_selected} Acum.'][-1]
valor_final_aportes = df_resultado['Aporte Acum.'][-1]

delta = str(round((valor_final_invest-valor_final_aportes)/valor_final_aportes * 100, 2)) + '%'
profit = 'R$' + str(round(valor_final_invest-valor_final_aportes, 2))

st.plotly_chart(result)

cols = st.columns(2)

with cols[0]:
    st.metric(label = 'Investido',
          value = 'R$' + str(round(valor_final_invest, 2)),
          delta = 'R$' + str(round(valor_final_aportes, 2)),)

with cols[1]:
    st.metric(label = 'Lucro',
          value = profit, 
          delta = delta,
          delta_color="normal")