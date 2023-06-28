import pytest
from os import path, getcwd

def test_files_exist():
  assert path.exists('./data/raw/cloudiness.csv')
  assert path.exists('./data/raw/extreme_wind.csv')
  assert path.exists('./data/raw/temperature.csv')
  assert path.exists('./data/raw/visibility.csv')
  assert path.exists('./data/raw/precipitation.csv')
  assert path.exists('./data/raw/wind.csv')
  assert path.exists('./data/raw/biketemp.csv')
