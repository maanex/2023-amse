import urllib.request
import zipfile
import pandas as pd
import os
from sqlalchemy import create_engine

URL = 'https://gtfs.rhoenenergie-bus.de/GTFS.zip'

cols = {
  'stop_id': int,
  'stop_name': str,
  'stop_lat': float,
  'stop_lon': float,
  'zone_id': int
}


if __name__ == '__main__':
  res = urllib.request.urlretrieve(URL)

  with zipfile.ZipFile(res[0], 'r') as file:
    file.extract('stops.txt')

  df = pd.read_csv('stops.txt', sep=',', usecols=cols.keys(), dtype=cols, encoding='utf-8')
  os.remove('stops.txt')

  df = df.dropna()
  df = df[df['zone_id'] == 2001]
  df = df[df['stop_lat'] <= 90]
  df = df[df['stop_lat'] >= -90]
  df = df[df['stop_lon'] <= 90]
  df = df[df['stop_lon'] >= -90]

  engine = create_engine('sqlite:///gtfs.sqlite')
  df.to_sql('stops', engine, if_exists='replace', index=False)
