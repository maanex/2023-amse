import pytest
from os import path

def test_files_exist():
  assert path.exists('./raw/cloudiness.csv')
  assert path.exists('./raw/extreme_wind.csv')
  assert path.exists('./raw/temperature.csv')
  assert path.exists('./raw/visibility.csv')
  assert path.exists('./raw/precipitation.csv')
  assert path.exists('./raw/wind.csv')
  assert path.exists('./raw/biketemp.csv')
