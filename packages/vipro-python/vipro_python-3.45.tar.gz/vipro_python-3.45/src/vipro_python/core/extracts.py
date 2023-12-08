import pandas as pd
import os

def read_first_n_lines(file_path, n) -> str:
  res = []
  with open(file_path, 'r') as file:
    for _ in range(n):
      line = file.readline()
      if not line:
        break
      res.append(line.strip())
  return '\n'.join(res)

def detect_delimiter(input: str) -> str:
  delimiter = ','
  commas_count = input.count(',')
  pipes_count = input.count('|')
  tabs_count = input.count('\t')
  top_scorer = max(commas_count, pipes_count, tabs_count)
  if pipes_count == top_scorer:
    delimiter = '|'
  elif tabs_count == top_scorer:
    delimiter = '\t'
  return delimiter

def read_extract(file_name: str) -> pd.DataFrame:
  df = None
  extension = os.path.splitext(file_name)[1].lower()
  print(f"extension detected: {extension}")

  if extension == '.xlsx':
    df = read_excel(file_name)
    pass
  else:
    df = read_csv(file_name)
  
  # happy path :)
  return df


def read_excel(file_name: str) -> pd.DataFrame:
  # TODO: read spreadsheet
  raise Exception(f"could not extract file: {file_name}")


def read_csv(file_name: str) -> pd.DataFrame:
  # this is probably a text-based flat-file
  # TODO: skip rows
  first_lines = read_first_n_lines(file_name, 4)
  delimiter = detect_delimiter(first_lines)
  print(f"delimiter used: {delimiter}")
  return pd.read_csv(file_name, delimiter=delimiter, dtype=str, engine='python', encoding='cp437')