import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from EyeTrackingPackage.modules.python.utils.values_checker import ValuesChecker


def get_trajectory_as_df(path, settings):
    """Loads path as csv data frame via pandas.read_csv with additional parameters from settings

    :param path: csv-file to read from
    :param settings: settings dictionary of proper format (see docs)
    :return: coordinates data frame
    :rtype: pandas.DataFrame
    """
    ValuesChecker.check_settings(settings)
    reading_settings = settings['loading']
    df = pd.read_csv(path, **reading_settings)

    colnames = df.columns
    columns = dict()
    for a, b in settings['columns'].items():
        if type(b) is int:
            columns[colnames[b]] = a
        else:
            columns[b] = a

    cols_to_select = list(settings['columns'].keys())

    df = df.rename(columns=columns)

    if settings['common']['adjust_time']:
        min_t = np.min(df.loc[:, 'time'])
        df.loc[:, 'time'] = df.loc[:, 'time'] - min_t

    if settings['common']['normalized']:
        df.loc[:, ['porx', 'pory']] = df.loc[:, ['porx', 'pory']] * np.array(settings['common']['resolution'])

    return df[cols_to_select]


def smooth_trajectory_df(df, settings=None):
    """Performs data frame coordinates smoothing with one of three (currently) methods:
    - median smoothing
    - moving average smoothing
    - Savitzky-Golay signal filtering

    :param df: coordinates data frame
    :param settings: settings dictionary with filled smoothing field
    :return: smoothed data frame
    :rtype: pandas.DataFrame
    """
    df = df.copy()
    if settings['smoothing'] is None:
        return df
    else:
        df = df.copy()
        cols_to_smooth = df.drop('time', 1).columns
        windows = df.loc[:, cols_to_smooth].rolling(window=settings['smoothing']['window'],
                                                    center=settings['smoothing']['center'])
        if settings['smoothing']['method'] in ['med', 'median']:
            windows = windows.median()
        elif settings['smoothing']['method'] in ['avg', 'average', 'mean']:
            windows = windows.mean()
        else:
            windows = df[cols_to_smooth].apply(lambda x: savgol_filter(x,
                                                                       window_length=settings['smoothing']['window'],
                                                                       polyorder=settings['smoothing']['order']),
                                               axis=0)
        df.loc[:, cols_to_smooth] = windows
        if settings['smoothing']['fillna']:
            df = df.fillna(method='bfill').fillna(method='ffill')
        return df


def calculate_angular_parameters(df, settings):
    """Performs angular parameters calculation for input coordinates data frame

    :param df: coordinates data frame
    :param settings: settings dictionary with filled common field
    :return: data frame with additional parameters
    :rtype: pandas.DataFrame
    """
    df = df.copy()
    d = settings['common']['distance']
    wid, hei = settings['common']['size']
    wpix, hpix = settings['common']['resolution']

    if settings['common']['reference_point'] is None:
        refx, refy = wid/2, hei/2
    else:
        refx, refy = settings['common']['reference_point']

    df['dt'] = df['time'].diff()
    # Angular coordinates
    df['xAng'] = 180 / np.pi * np.arctan((df.porx - refx) / (d * wpix / wid))
    df['yAng'] = 180 / np.pi * np.arctan((df.pory - refy) / (d * hpix / hei))
    # Angular velocity
    if settings['common']['velocity_type'] == 'finite_difference':
        df['distAng'] = np.sqrt(np.sum(df[['xAng', 'yAng']].diff()**2, 1))
    else:
        xdash = savgol_filter(x=df['xAng'].values,
                              window_length=settings['smoothing']['window'],
                              polyorder=2,
                              deriv=1)
        ydash = savgol_filter(x=df['yAng'].values,
                              window_length=settings['smoothing']['window'],
                              polyorder=2,
                              deriv=1)
        df['distAng'] = np.sqrt(xdash**2 + ydash**2)

    df['velAng'] = df['distAng'] / df['dt']
    df['accelAng'] = df['velAng'].diff() / df['dt']

    df.loc[:, ['velAng', 'accelAng']] = df[['velAng', 'accelAng']].replace(to_replace=[np.nan, np.inf, -np.inf], value=0)

    return df


def IVT(df, settings):
    df = df.copy()
    df['above_threshold'] = df['velAng'] > settings['oculus']['velocity_threshold']
    df['event'] = df['above_threshold'].replace([True, False], ['Saccade', 'Fixation'])
    return df.drop('above_threshold', 1)
