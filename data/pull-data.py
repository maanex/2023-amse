import urllib.request
import zipfile
import os
import os.path as path
import glob
import csv
import json
from rich.progress import track


RAW_DATA_FOLDER = './raw/'
OUT_DATA_FOLDER = './out/'

WEATHER_URLS = [
  ('cloudiness', 'produkt_n_stunde_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/cloudiness/historical/stundenwerte_N_01766_19891001_20221231_hist.zip'),
  ('extreme_wind', 'produkt_fx_stunde_19900701_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/extreme_wind/historical/stundenwerte_FX_01766_19900701_20221231_hist.zip'),
  ('moisture', 'produkt_tf_stunde_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/moisture/historical/stundenwerte_TF_01766_19891001_20221231_hist.zip'),
  ('temperature', 'produkt_tu_stunde_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/stundenwerte_TU_01766_19891001_20221231_hist.zip'),
  ('visibility', 'produkt_vv_stunde_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/visibility/historical/stundenwerte_VV_01766_19891001_20221231_hist.zip'),
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
  with open(filename, 'wb') as out:
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
  for year in range(2020, 2021):
    for month in track(range(1, 13), description=f'Downloading weather for {year}'):
      download_and_process_bike(month, year)

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
  write_file(path.join(RAW_DATA_FOLDER, 'bikedata.json'), json.dumps(data))

#

def main(skipdownload=False):
  if not skipdownload:
    clear_folder(RAW_DATA_FOLDER, '*')
    download_weather_urls()
    clear_folder(RAW_DATA_FOLDER, '*.zip')

  # cloudiness    = parsefile_weather('cloudiness',   lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), int(a[3]), int(a[4])))
  # extreme_wind  = parsefile_weather('extreme_wind', lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), float(a[3])))
  # moisture      = parsefile_weather('moisture',     lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), float(a[3]), int(a[4]), float(a[5]), float(a[6])))
  # temperature   = parsefile_weather('temperature',  lambda a: a[1].startswith('20'), lambda a: (int(a[1]), float(a[2]), float(a[3])))
  # visibility    = parsefile_weather('visibility',   lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), int(a[3])))
  # wind          = parsefile_weather('wind',         lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), int(a[3]), int(a[4])))

  download_and_process_bike_all_months()


if __name__ == '__main__':
  main(True)
