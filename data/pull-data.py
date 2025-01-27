import urllib.request
import zipfile
import os
import os.path as path
import glob
import csv
import json
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from rich.progress import track


RAW_DATA_FOLDER = './raw/'
OUT_DATA_FOLDER = './out/'

WEATHER_URLS = [
  ('cloudiness', 'produkt_n_stunde_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/cloudiness/historical/stundenwerte_N_01766_19891001_20221231_hist.zip'),
  ('extreme_wind', 'produkt_fx_stunde_19900701_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/extreme_wind/historical/stundenwerte_FX_01766_19900701_20221231_hist.zip'),
  ('temperature', 'produkt_tu_stunde_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/stundenwerte_TU_01766_19891001_20221231_hist.zip'),
  ('visibility', 'produkt_vv_stunde_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/visibility/historical/stundenwerte_VV_01766_19891001_20221231_hist.zip'),
  ('precipitation', 'produkt_rr_stunde_19950901_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/precipitation/historical/stundenwerte_RR_01766_19950901_20221231_hist.zip'),
  ('wind', 'produkt_ff_stunde_19820101_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/wind/historical/stundenwerte_FF_01766_19820101_20221231_hist.zip'),
]

BIKE_IDS = [ '100034978', '100031300', '100034980', '100034982', '100053305', '100035541', '100031297', '100034983', '100034981' ]
BIKE_URL_BASE = 'https://raw.githubusercontent.com/od-ms/radverkehr-zaehlstellen/main/'




def clear_folder(path, match = '*'):
  [ os.remove(f) for f in glob.glob(os.path.join(path, match)) ]

def download_file(url, output):
  with urllib.request.urlopen(url) as web:
    write_file(path.join(RAW_DATA_FOLDER, output), web.read())

def write_file(filename, data):
  with open(filename, 'w' if filename.endswith('json') else 'wb') as out:
    out.write(data)

#

def extract_file(zippath, filename):
  archive = zipfile.ZipFile(path.join(RAW_DATA_FOLDER, zippath), 'r')
  filedata = archive.read(filename)
  return filedata

def download_weather_urls():
  for (cleanname, filename, url) in track(WEATHER_URLS, description='Downloading files...'):
    download_file(url, cleanname + '.zip')
    raw = extract_file(cleanname + '.zip', filename)
    write_file(path.join(RAW_DATA_FOLDER, cleanname + '.csv'), raw)

def parsefile_weather(filename, filter, parser):
  out = []
  with open(path.join(RAW_DATA_FOLDER, filename + '.csv'), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)
    for row in reader:
      if filter(row):
        out.append(parser(row))
  return out

#

def download_and_process_bike_all_months():
  out = []
  for year in range(2020, 2022):
    for month in track(range(1, 13), description=f'Downloading bike for {year}'):
      for entry in download_and_process_bike(month, year):
        out.append(entry)
  return out

def download_and_merge_bike(url, statid, data):
  download_file(url, 'biketemp.csv')

  with open(path.join(RAW_DATA_FOLDER, 'biketemp.csv'), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    hourcount = 0
    for row in reader:
      daytime = row[0]
      count = row[1]
      (day, time) = daytime.split(' ')
      (hour, minute) = time.split(':')
      if minute == '45':
        key = f'{day} {hour}'
        if not key in data:
          data[key] = {}
        data[key][statid] = hourcount
        hourcount = 0
      else:
        hourcount += int(count)

def download_and_process_bike(month, year):
  date = f'{year}-{month:02d}'
  data = {}
  for statid in BIKE_IDS:
    download_and_merge_bike(BIKE_URL_BASE + statid + '/' + date + '.csv', statid, data)

  out = []
  for time in data.keys():
    temp, hour = time.split(' ')
    year, month, day = temp.split('-')
    date = int(year + month + day + hour)
    out.append({
      'id': time,
      'date': date,
      'count': sum(data[time].values())
    })

  return out

def merge_weather_data(cloudiness, extreme_wind, temperature, visibility, precipitation, wind):
  vals = {}

  for date, v1 in cloudiness:
    if not date in vals: vals[date] = {}
    vals[date]['clouds_vn'] = v1
  for date, v1 in extreme_wind:
    if not date in vals: vals[date] = {}
    vals[date]['ewind_fx911'] = v1
  for date, v1, v2 in temperature:
    if not date in vals: vals[date] = {}
    vals[date]['temp_tt_tu'] = v1
    vals[date]['temp_rf_tu'] = v2
  for date, v1 in visibility:
    if not date in vals: vals[date] = {}
    vals[date]['vis_v_vv'] = v1
  for date, v1 in precipitation:
    if not date in vals: vals[date] = {}
    vals[date]['prec_r1'] = v1
  for date, v1, v2 in wind:
    if not date in vals: vals[date] = {}
    vals[date]['wind_f'] = v1
    vals[date]['wind_d'] = v2

  out = [ 'date;clouds_vn;ewind_fx911;temp_tt_tu;temp_rf_tu;vis_v_vv;prec_r1;wind_f;wind_d' ]
  for k in vals:
    v = vals[k]
    out.append(';'.join(map(str, [
      k,
      v.get('clouds_vn', 0),
      v.get('ewind_fx911', 0),
      v.get('temp_tt_tu', 0),
      v.get('temp_rf_tu', 0),
      v.get('vis_v_vv', 0),
      v.get('prec_r1', 0),
      v.get('wind_f', 0),
      v.get('wind_d', 0)
    ])))

  return '\n'.join(out)

#

def main(skipdownload=False):
  if not skipdownload:
    clear_folder(RAW_DATA_FOLDER, '*')
    download_weather_urls()
    clear_folder(RAW_DATA_FOLDER, '*.zip')

  cloudiness    = parsefile_weather('cloudiness',    lambda a: a[1].startswith('202'), lambda a: (int(a[1]), int(a[4])))
  extreme_wind  = parsefile_weather('extreme_wind',  lambda a: a[1].startswith('202'), lambda a: (int(a[1]), float(a[3])))
  temperature   = parsefile_weather('temperature',   lambda a: a[1].startswith('202'), lambda a: (int(a[1]), float(a[3]), float(a[4])))
  visibility    = parsefile_weather('visibility',    lambda a: a[1].startswith('202'), lambda a: (int(a[1]), float(a[4])))
  precipitation = parsefile_weather('precipitation', lambda a: a[1].startswith('202'), lambda a: (int(a[1]), float(a[3])))
  wind          = parsefile_weather('wind',          lambda a: a[1].startswith('202'), lambda a: (int(a[1]), float(a[3]), int(a[4])))

  weather_merged = merge_weather_data(cloudiness, extreme_wind, temperature, visibility, precipitation, wind)

  with open('raw/weather_merged.csv', 'w') as out:
    out.write(weather_merged)

  engine = create_engine('sqlite:///data.sqlite')

  weather_pd = pd.read_csv(StringIO(weather_merged), sep=';')
  weather_pd.to_sql('weather', engine, if_exists='replace', index=False)

  #

  bike_data = download_and_process_bike_all_months()

  metadata = MetaData()
  columns = [
    Column('id', String, primary_key=True),
    Column('date', Integer),
    Column('count', Integer)
  ]
  table = Table('bikes', metadata, *columns)

  metadata.create_all(bind=engine)

  with engine.connect() as conn:
    conn.execute(table.insert(), bike_data)
    conn.commit()

  print('Done')

if __name__ == '__main__':
  main()
