import pytest
from os import path, getcwd

def test_files_exist():
  print(getcwd())
  print(getcwd())
  print(getcwd())
  print(getcwd())
  print(getcwd())
  print(getcwd())
  assert path.exists(getcwd() + '/data/raw/cloudiness.csv')
  assert path.exists(getcwd() + '/data/raw/extreme_wind.csv')
  assert path.exists(getcwd() + '/data/raw/temperature.csv')
  assert path.exists(getcwd() + '/data/raw/visibility.csv')
  assert path.exists(getcwd() + '/data/raw/precipitation.csv')
  assert path.exists(getcwd() + '/data/raw/wind.csv')
  assert path.exists(getcwd() + '/data/raw/biketemp.csv')
