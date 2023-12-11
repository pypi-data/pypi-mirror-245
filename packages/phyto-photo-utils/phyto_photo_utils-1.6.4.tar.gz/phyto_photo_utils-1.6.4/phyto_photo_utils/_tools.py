#!/usr/bin/env python

import numpy as np
import pandas as pd
from datetime import timedelta

def remove_outlier_from_time_average(df, time=4, multiplier=3):
    """
    
    Remove outliers when averaging transients before performing the fitting routines, used to improve the signal to noise ratio in low biomass systems.

    The function sets a time window to average over, using upper and lower limits for outlier detection.
    The upper and lower limits are determined by mean ± std x [1].
    The multiplier [1] can be adjusted by the user.

    Parameters
    ----------
    df : pandas.DataFrame
        A dataframe of the raw data, can either be imported from pandas.read_csv or the output from phyto_photo_utils.load
    time : int, default=4
     	The time window to average over, e.g. 4 = 4 minute averages
    multiplier : int, default=3	
        The multiplier to apply to the standard deviation for determining the upper and lower limits.

    Returns
    -------
    df : pandas.DataFrame 
        A dataframe of the time averaged data with outliers excluded.

    Example
    -------
    >>> ppu.remove_outlier_from_time_average(df, time=2, multiplier=3)

    """

    # Convert time window to string
    dt = str(time)+'T'
    # Convert dtype of the datetime column
    df['datetime'] = df.datetime.astype('datetime64')
    
    # Group data by time window and flashlet number
    grouped = df.groupby([pd.Grouper(key='datetime', freq=dt), 'flashlet_number'])
    
    # Calculate means, standard deviations and counts of the groups
    grouped_mean = grouped.mean()
    grouped_std = grouped.std()
    grouped_counts = grouped.count()
    
    # Calculate upper and lower limits of each group, and repeat each value by its count
    ulim = (grouped_mean['flevel'] + grouped_std['flevel'] * multiplier).repeat(grouped_counts['flevel'])
    llim = (grouped_mean['flevel'] - grouped_std['flevel'] * multiplier).repeat(grouped_counts['flevel'])

    # Get indexes of data used to create each group
    idx = [items[-1] for items in grouped.indices.items()]
    idx = np.concatenate(idx, axis=0)

    # Create pandas DataFrame of upper and lower using original indexes of data
    mask = pd.DataFrame({'ulim': ulim, 'llim': llim, 'index': idx})
    mask = mask.set_index('index').sort_index()

    # Create boolean array using mask DataFrame
    m = (df['flevel'] > mask['ulim']) | (df['flevel'] < mask['llim'])
    
    # Where condition is True, set values of fluorescence yield to NaN
    df.loc[m.values,'flevel'] = np.nan

    # Group data that is now corrected
    df = df.groupby([pd.Grouper(key='datetime', freq=dt), 'flashlet_number']).mean().reset_index()
    
    # Return number of measurements that is used to create each average
    df['nseq'] = grouped_counts['flevel'].values
    
    return df

def correct_fire_instrument_bias(df, pos=1, sat_len=100):
    
    """
    
    Corrects for instrumentation bias in the relaxation phase by calculating difference between flashlet 0 of the relaxation phase & flashlet[pos].
    This bias is then added to the relaxation phase.

    Parameters
    ----------
    df : pandas.DataFrame 
        A dataframe of the raw data, can either be imported from pandas.read_csv or the output from phyto_photo_utils.load
    pos : int, default=1
     	The flashlet number after the start of the relaxation phase, to calculate difference between.
    sat_len : int, default=100
     	The length of saturation measurements.

    Returns
    -------
    df : pandas.DataFrame 
        A dataframe of FIRe data corrected for the instrument bias.

    Example
    -------
    >>> ppu.correct_fire_bias_correction(df, pos=1, sat_len=100)

    """

    flevel = np.array(df.flevel)
    seq = np.array(df.seq)
    
    corrected_data = []
    
    for unique_seq in np.unique(seq):
        # Filter data based on the unique measurement number
        mask = seq == unique_seq
        data = flevel[mask]
        
        # Calculate the correction value
        correction = data[sat_len - pos] - data[sat_len]
        
        # Apply the correction to data
        data[sat_len:] += correction
        
        corrected_data.append(data)
    
    # Reshape the corrected data
    corrected_data = np.array(corrected_data)
    corrected_data = np.reshape(corrected_data, (corrected_data.shape[0] * corrected_data.shape[1]))
    
    # Replace fluorescence levels in the DataFrame with the bias-corrected data
    df['flevel'] = corrected_data
    
    return df

def calculate_blank_FastOcean(file_, seq_len=100, delimiter=','):
     
    """
    Calculates the blank by averaging the fluorescence level for the saturation phase.

    Parameters
    ----------
    file_ : str
        The path directory to the raw blank file in csv format.
    seq_len : int, default=100
        The length of the measurement sequence.
    delimiter : str, default=','
        Specify the delimiter to be used by Pandas.read_csv for loading the raw files.
    
    Returns
    -------
    res : pandas.DataFrame
        The blank results.

    Example
    -------
    >>> ppu.calculate_blank_FastOcean(file_, seq_len=100)
    """

    df = pd.read_csv(file_, skiprows=26, nrows=2, header=None, delimiter=delimiter, encoding='latin1')
    df = df.iloc[:, 2:].T
    df.columns = ['date', 'time']
    df['datetime'] = pd.to_datetime(df['date']+' '+df['time'])
    df = df.drop(columns=['date', 'time'])

    res = pd.read_csv(file_, skiprows=43, nrows=seq_len, header=None, delimiter=delimiter, encoding='latin1')
    res = res.iloc[:, 2:]
    res = res.agg(['mean', 'std']).T
    res.columns = ['blank_mean', 'blank_stdev']
    res = pd.DataFrame(res)
    res['datetime'] = df['datetime']

    return res

def calculate_blank_FIRe(file_):

    """
    Calculates the blank by averaging the fluorescence level for the saturation phase.

    Parameters
    ----------
    file_ : str
        The path directory to the raw blank file.

    Returns
    -------
    res : pandas.DataFrame
        The blank results: blank, datetime

    Example
    -------
    >>> ppu.calculate_blank_FIRe(file_)
    """

    # Read the CSV file into a DataFram
    df = pd.read_csv(file_)
    
    # Extract date and time information from the first row
    datetime_info = str(df.iloc[0,:].values).strip()[2:-2].split('  ')
    date = datetime_info[0].strip()
    time = datetime_info[-1].strip()
    time = str(timedelta(seconds=int(time)))
    datetime_str = date+' '+time
    datetime_format = '%m/%d/%Y %H:%M:%S'
    dt = pd.to_datetime(datetime_str, format=datetime_format)

    # Get saturation phase length from the file
    sat_len = int(str(df.iloc[5,:].values[0]).split()[-1][:-2])

    # Read in the actual data from the CSV file
    data_df = pd.read_csv(file_, index_col=0, skiprows=20, header=None, delim_whitespace=True)
    data_df.columns = ['time', 'ex', 'flevel']
    
    # Calculate the mean and standard deviation of 'flevel' for the first 'sat_len' rows
    blank = data_df['flevel'][:sat_len].mean(axis=0)
    stdev = data_df['flevel'][:sat_len].std(axis=0)
    
    # Create a DataFrame with the extracted data
    data = {
    'datetime': [datetime],
    'blank_mean': [blank_mean],
    'blank_stdev': [blank_stdev]
    }
    res = pd.DataFrame(data)

    return res

