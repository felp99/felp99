from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import gspread
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'start':1,
    'limit': '5000',
    'convert': 'BRL'
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': #SUA CHAVE AQUI,
}

session = Session()
session.headers.update(headers)

response = session.get(url, params=parameters)
data = json.loads(response.text)

df = pd.DataFrame(data['data'])
info = (df['quote'].apply(pd.Series)['BRL']).apply(pd.Series)
to_sheet = df[['name', 'symbol', 'slug']]
to_sheet = pd.merge(to_sheet, info, left_index=True, right_index=True)
to_sheet = to_sheet.fillna('')

gc = gspread.service_account(filename = 'key.json')
code = '1F9NY5hQQQozC5MGuseiDxpj218902He_Gna-doOrobs'
sh = gc.open_by_key(code)
ws = sh.worksheet('CoinMarketCap')
clear = ws.clear()

update = ws.update([to_sheet.columns.values.tolist()] + to_sheet.values.tolist())