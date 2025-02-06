import os
import pandas as pd
import numpy as np
import statistics as stats


#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

# Functions for combining data script

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

# Functions for QC flaggings script

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

def convert_to_num(in_df):
  ''' forces data type number on values in dataframe columns'''
  for col in list(in_df.columns)[3:]:
    in_df[col]=pd.to_numeric(in_df[col], errors='coerce')
  return in_df

def assign_datetime_index(df_in):
  ''' for plotting in bokeh'''
  df_in['date_time'] = pd.to_datetime(df_in['date_time'])
  return df_in


def rolling_quantile_flagging(in_df, _var_ = 'LE',verbose=False):
    '''
    applies a rolling 30 day quantile filter to remove outlies not detected by the spike removal alogirthm
    2.5 x the inter quartile range is applied to Q1 and Q3 to detect anomalous outliers
    '''
    
    flag_id = _var_ + '_pi_flag'
    if flag_id in in_df.columns:
      if verbose ==True:
        print(flag_id + ' already created')
    else:
      print('creating '+flag_id)
      in_df[flag_id]='good'

    df=in_df.copy()
    df[_var_]= (np.array(pd.to_numeric(df[_var_], errors='coerce')))
    df.set_index('date_time',inplace=True)
    df = df[~df.index.duplicated(keep='first')]
    df['IQR']=df[_var_].rolling('15D',min_periods=30).quantile(0.75)-df[_var_].rolling('30D',min_periods=30).quantile(0.25)
    df['max']=df['IQR']*2.5+df[_var_].rolling('15D',min_periods=30).quantile(0.75)
    df['min']=df[_var_].rolling('15D',min_periods=30).quantile(0.25)-df['IQR']*2.5
    df.loc[df[_var_] > df['max'], flag_id] = 'bad'
    df.loc[df[_var_] < df['min'], flag_id] = 'bad'
    df.drop(['IQR','max','min'],inplace=True,axis=1)

    # returns the dataframe without the min / max thresholds used to trim
    return df.reset_index()

def flag_spikes(in_df, _var_='LE', z = 6.5,verbose=True):
    '''
    This function removes spikes or anomalies in data for ameriflux data
    The outlider detection method followsthe median of absolute deviation about the median
    See Papale et al., 2006 | Towards a standardized processing of Net Ecosystem Exchange
        measured with eddy covariance technique: algorithms and uncertainty estimation
        https://bg.copernicus.org/articles/3/571/2006/
    inputs:
    in_df: dataframe with both LE & NETRAD (e.g. standard Ameriflux Names)
    varnames: List of variables to filter, default parameter set to LE
    z: larger numbers are more conservative and default follows guidance in Papale et al., 2006
    '''
    
    in_df[_var_]= (np.array(pd.to_numeric(in_df[_var_], errors='coerce')))

    df_temp=in_df.copy()
    df_temp.set_index('date_time',inplace=True)
    df_temp = df_temp[~df_temp.index.duplicated(keep='first')]

    flag_id = _var_ + '_pi_flag'

    if flag_id in df_temp.columns:
      if verbose ==True:
        print(flag_id + ' already created')
    else:
      print('creating '+flag_id)
      in_df[flag_id]='good'

    df_temp['NETRAD']=(np.array(pd.to_numeric(df_temp['NETRAD'], errors='coerce')))
    df_day = df_temp[(df_temp.NETRAD > 0)|(df_temp.NETRAD.isnull()) & ((df_temp.index.hour>=6)&(df_temp.index.hour<18))]
    df_night= df_temp[(df_temp.NETRAD <= 0)|(df_temp.NETRAD.isnull()) & ((df_temp.index.hour < 6) | ((df_temp.index.hour >= 18)))]

    di_n = df_night[_var_].diff()-(df_night[_var_].diff(periods=-1)*-1.0)
    di_d = df_day[_var_].diff()-(df_day[_var_].diff(periods=-1)*-1.0)
    md_n = np.nanmedian(di_n)
    md_d = np.nanmedian(di_d)
    mad_n = np.nanmedian(np.abs(di_n-md_n))
    mad_d = np.nanmedian(np.abs(di_d-md_d))

    # mask night data for high and low anomalies and filter for spikes
    mask_nh = di_n < md_n - (z*mad_n/0.6745)
    mask_nl = di_n > md_n + (z*mad_n/0.6745)
    df_night.loc[mask_nh|mask_nl,_var_]=np.nan
    # df_night[_var_][mask_nh|mask_nl]=np.nan

    # mask daytime data for high and low anomalies and filter for spikes
    mask_dh = di_d < md_d - (z*mad_d/0.6745)
    mask_dl = di_d > md_d + (z*mad_d/0.6745)
    df_day.loc[mask_dh|mask_dl,_var_]=np.nan
    # df_day[_var_][mask_dh|mask_dl]=np.nan

    df_out = pd.concat([df_night, df_day],verify_integrity=True).sort_index()
    in_df[_var_+'temp'] = np.array(df_out[_var_])

    in_df.loc[np.isnan(np.array(in_df[_var_+'temp'])), flag_id] = 'bad'
    in_df.drop(columns=[_var_+'temp'],axis=1,inplace=True)
    # returns the dataframe with the 'bad flag appended to the column
    return in_df

def flag_by_wind_dir(in_df, low_wd=180,high_wd=180):
    '''
    flags data by wind directions > low_wd AND < high_wd]
    returns the dataframe with the 'bad flag appended to the column
    '''

    in_df['WD']= (np.array(pd.to_numeric(in_df['WD'], errors='coerce')))
    flag_id = 'LE_pi_flag'
    in_df.loc[(in_df['WD']<high_wd)&(in_df['WD']>low_wd), flag_id] = 'bad'
    return in_df

def date_flag(in_df, col_name, start_date, end_date, status):
    '''
    applies a qc flag to a set column for a specific date range
    args:
    in_df: input dataframe
    col_name: qc_flag column name
    start_date: fmt %Y-%m-%d (inclusive in flag)
    end_date: fmt %Y-%m-%d (exclused from flag)
    status: good or bad, or another custom value e.g. pi
    '''
    
    in_df.set_index('date_time',inplace=True)
    after_start = in_df.index >= start_date
    before_end = in_df.index < end_date
    in_df.loc[after_start & before_end, col_name] = status
    return in_df.reset_index()


def date_HH_flag(in_df, col_name, start_date, end_date, status):
    '''
    applies a qc flag to a set column for a specific date range with hours

    args:
    in_df: input dataframe
    col_name: qc_flag column name
    start_date: fmt %Y-%m-%d-%hh:mm
    end_date: fmt %Y-%m-%d-%hh:mm
    status: good or bad, or another custom value e.g. pi
    '''

    in_df.set_index('date_time',inplace=True)
    after_start = in_df.index >= start_date
    before_end = in_df.index < end_date
    in_df.loc[after_start & before_end, col_name] = status
    return in_df.reset_index()

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

# functions to calculate statistics (edited on 2/5/25)

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

def filter_nan(s,o):
        """
        this functions removed the data  from simulated and observed data
        whereever the observed data contains nan

        this is used by all other functions, otherwise they will produce nan as
        output
        """
        import numpy as np
        data = np.array([s,o])
        data = np.transpose(data)
        data = data[~np.isnan(data).any(1)]
        return data[:,0],data[:,1]

def rmse(s,o):
        """
        Root Mean Squared Error
        input:
                s: simulated
                o: observed
        output:
                rmses: root mean squared error
        """
        import numpy as np
        s,o = filter_nan(s,o)
        return np.sqrt(np.mean((s-o)**2))

def no_nans(A1, A2):
    ''' returns the mask of nans for 2 arrays'''
    import numpy as np
    mask = ~np.isnan(A1) & ~np.isnan(A2)
    return mask

def R2_fun(s,o):
    """
    R^2 or Correlation coefficient^0.5
    input:
            s: simulated
            o: observed
    output:
            R^2
    """
    import numpy as np
    from scipy import stats
    if ((o == o[0]).all())|((s == s[0]).all()):
        r2_o_d_=np.nan
    else:
        m_o_d = no_nans(np.array(o),np.array(s))
        if len(np.array(o)[m_o_d])==0 | len(np.array(s)[m_o_d])==0:
            r2_o_d_ = np.nan
        else:
            stats_o_d = stats.linregress(np.array(o)[m_o_d],np.array(s)[m_o_d])
            slope_o_d = stats_o_d[0];
            int_o_d = stats_o_d[1];
            r2_o_d_ = stats_o_d[2]**2

    return r2_o_d_, slope_o_d, int_o_d

def get_slope(s,o):
    """
    returns slope through origin
    input:
            s: simulated
            o: observed
    output:
            slope
    """
    import numpy as np
    from scipy import stats
    if ((o == o[0]).all())|((s == s[0]).all()):
        r2_o_d_=np.nan
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

