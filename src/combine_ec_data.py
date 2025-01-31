import os
import pandas as pd
import numpy as np

def get_field_name(raw_data_path):
  '''
  extracting the field name from a folder path for file naming
  '''
  elements= raw_data_path.split('/')[-2].split('_')
  if len(elements)>=3:
    field_name = '_'.join(elements[:-1])
  else:
    field_name = elements[0]
  return(field_name)
  
def check_folder(data_path, out_path):
  '''
  check if folders are present
  if not present, folders are created
  '''
  if os.path.exists(data_path):
      print("{0} folder exists...".format(data_path))
      if not os.path.exists(out_path):
          print('\tcan not locate {0} ...'.format(out_path))
          print('\tmaking directory: {0} ... '.format(out_path))
          os.mkdir(out_path)
          print("\tdirectory {0} created".format(out_path))
      else:
          print("{0} folder exists...".format(out_path))
  else:
      raise FileNotFoundError("{0} folder does not exist! Check data_path.".format(data_path))


def set_time_index(df_in):
  '''
  assigns datetime column
  '''
  df_in['date_time'] = pd.to_datetime(df_in['TIMESTAMP_START'].astype('int'), format='%Y%m%d%H%M');
  df_in.set_index(['date_time'],inplace=True);
  return df_in


def to_numeric(df_time):
  '''
  converts dataframe from object to numeric data
  corrupt cells will be assigned NaN values
  '''
  df_numeric = df_time.copy()
  for col in list(df_time.columns):
    df_numeric[col]=(np.array(pd.to_numeric(df_time[col], errors='coerce')))
  return df_numeric.resample('30min').mean()

def check_for_missing_columns(df_i, col_list):
  '''
  assigns null values to temp, humidty, dew point when HMP155 is turned off
  '''
  missing_cols = set(col_list).difference(set(df_i.columns.unique()))

  for col in missing_cols:
    df_i[col]=np.nan

  return df_i