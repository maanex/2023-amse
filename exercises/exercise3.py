import pandas as pd
from sqlalchemy import create_engine, types

url = 'https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv'

columns = {
  0: 'date',
  1: 'CIN',
  2: 'name',
  12: 'petrol',
  22: 'diesel',
  32: 'gas',
  42: 'electro',
  52: 'hybrid',
  62: 'plugInHybrid',
  72: 'others',
}

numcols = [
  'petrol',
  'diesel',
  'gas',
  'electro',
  'hybrid',
  'plugInHybrid',
  'others'
]

if __name__ == '__main__':
  csv = pd.read_csv(url, sep=';', engine='python', skiprows=7, skipfooter=4, usecols=columns.keys(), names=columns.values(), dtype=dict.fromkeys(columns.values(), str), encoding='latin')

  csv = csv[csv['CIN'].str.match('^\d{5}$')]

  for col in numcols:
    csv[col] = pd.to_numeric(csv[col], downcast='integer', errors='coerce')
    csv = csv[csv[col] > 0]

  csv.dropna()

  engine = create_engine('sqlite:///cars.sqlite')
  csv.to_sql('cars', engine, if_exists='replace', index=False, dtype=dict.fromkeys(numcols, types.INTEGER))
