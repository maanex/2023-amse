import pandas as pd
from sqlalchemy import create_engine

if __name__ == '__main__':
  csv = pd.read_csv('https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv', sep=';')
  engine = create_engine('sqlite:///airports.sqlite')

  csv.to_sql('airports', engine, if_exists='replace', index=False)
