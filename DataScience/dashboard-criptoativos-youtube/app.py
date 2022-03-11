#pip install streamlit
#pip install yfinance
#pip install plotly
#pip install pandas numpy json datetime

import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import datetime
import json
import yfinance as yf


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

st.title(f'Valores de {crypto_selected}')
fig = px.line(df, 
              x = df.index, 
              y = 'Close')

st.plotly_chart(fig)