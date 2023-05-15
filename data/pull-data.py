import urllib.request
import zipfile
import os
import os.path as path
import glob
import csv
from rich.progress import track


RAW_DATA_FOLDER = './raw/'
OUT_DATA_FOLDER = './out/'

URLS = [
  ('cloudiness', 'produkt_n_termin_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/cloudiness/historical/terminwerte_N_01766_19891001_20221231_hist.zip'),
  ('extreme_wind', 'produkt_fx3_termin_19900701_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/extreme_wind/historical/terminwerte_FX3_01766_19900701_20221231_hist.zip'),
  ('moisture', 'produkt_tf_termin_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/moisture/historical/terminwerte_TF_01766_19891001_20221231_hist.zip'),
  ('temperature', 'produkt_tu_termin_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/historical/terminwerte_TU_01766_19891001_20221231_hist.zip'),
  ('visibility', 'produkt_vk_termin_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/visibility/historical/terminwerte_VK_01766_19891001_20221231_hist.zip'),
  ('wind', 'produkt_fk_termin_19891001_20221231_01766.txt', 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/wind/historical/terminwerte_FK_01766_19891001_20221231_hist.zip'),
]




def clear_folder(path, match = '*'):
  [ os.remove(f) for f in glob.glob(os.path.join(path, match)) ]

def download_file(url, output):
  with urllib.request.urlopen(url) as web:
    write_file(path.join(RAW_DATA_FOLDER, output), web.read())

def extract_file(zippath, filename):
  archive = zipfile.ZipFile(path.join(RAW_DATA_FOLDER, zippath), 'r')
  filedata = archive.read(filename)
  return filedata

def write_file(filename, data):
  with open(filename, 'wb') as out:
    out.write(data)

def download_urls():
  for (cleanname, filename, url) in track(URLS, description='Downloading files...'):
    download_file(url, cleanname + '.zip')
    raw = extract_file(cleanname + '.zip', filename)
    write_file(path.join(RAW_DATA_FOLDER, cleanname + '.csv'), raw)

#

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

def main(skipdownload=False):
  if not skipdownload:
    clear_folder(RAW_DATA_FOLDER, '*')
    download_urls()
    clear_folder(RAW_DATA_FOLDER, '*.zip')

  cloudiness    = parsefile_weather('cloudiness',   lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), int(a[3]), int(a[4])))
  extreme_wind  = parsefile_weather('extreme_wind', lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), float(a[3])))
  moisture      = parsefile_weather('moisture',     lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), float(a[3]), int(a[4]), float(a[5]), float(a[6])))
  temperature   = parsefile_weather('temperature',  lambda a: a[1].startswith('20'), lambda a: (int(a[1]), float(a[2]), float(a[3])))
  visibility    = parsefile_weather('visibility',   lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), int(a[3])))
  wind          = parsefile_weather('wind',         lambda a: a[1].startswith('20'), lambda a: (int(a[1]), int(a[2]), int(a[3]), int(a[4])))

  print(wind)


if __name__ == '__main__':
  main(True)
