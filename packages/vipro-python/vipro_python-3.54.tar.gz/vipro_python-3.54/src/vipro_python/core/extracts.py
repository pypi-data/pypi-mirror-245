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

  # all supported loaders
  if extension in ['.xlsx', '.xls']:
    engine = 'openpyxl' if extension == '.xlsx' else 'xlrd'
    df = read_excel(file_name, engine)
    pass
  else:
    df = read_csv(file_name)

  # strip spaces (think fixed-width columns)
  for col in df.columns:
    df[col] = df[col].str.strip()
  
  # happy path :)
  return df


def read_excel(file_name: str, engine: str) -> pd.DataFrame:
  for n in range(5):
    df = pd.read_excel(
      file_name,
      engine=engine,
      header=n,
      dtype=str,  
      index_col=False)
    if "Unnamed: 3" not in df.columns:
      print(f"found headers at row {n} (zero-indexed)")
      break
  return df


def read_csv(file_name: str) -> pd.DataFrame:
  # determine what the delimiter is
  first_lines = read_first_n_lines(file_name, 5)
  delimiter = detect_delimiter(first_lines)
  print(f"delimiter used: {delimiter}")
  # determine if we need to skip some silly header rows (i.e., Excel converted to CSV)
  skip_rows = csv_skip_rows(first_lines, delimiter)
  return pd.read_csv(
    file_name, 
    delimiter=delimiter, 
    skiprows=skip_rows, 
    dtype=str, 
    engine='python', 
    encoding='cp437', 
    index_col=False)


def csv_skip_rows(first_lines: str, delimiter: str) -> int:
  skip = 0
  lines = first_lines.split('\n')
  for line in lines:
    cells = [x.strip() for x in line.split(delimiter)]
    if len(cells) > 1 and (cells[0] != ''):
      return skip
    skip += 1
  return skip
