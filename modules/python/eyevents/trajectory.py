import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from eyevents.values_checker import ValuesChecker


class Trajectory:
    def __init__(self, path, settings):
        ValuesChecker.check_settings(settings)
        self.settings = settings.copy()
        self.path = path
        buf = path.replace('..', '_').split('.')
        if len(buf) < 2:
            self.name = path.split('/')[-1].split('\\')[-1]
        else:
            self.name = '_'.join(buf[:-1]).split('\\')[-1].split('/')[-1]
        self.raw_df = None
        self.df = None
        self.get_trajectory_as_df()
        self.smooth_trajectory_df()
        self.calculate_angular_parameters()

    def get_trajectory_as_df(self):
        """Loads path as csv data frame via pandas.read_csv with additional parameters from settings

        :return: coordinates data frame
        :rtype: pandas.DataFrame
        """
        reading_settings = self.settings['loading']
        df = pd.read_csv(self.path, **reading_settings)

        colnames = df.columns
        columns = dict()
        for a, b in self.settings['columns'].items():
            if type(b) is int:
                columns[colnames[b]] = a
            else:
                columns[b] = a

        cols_to_select = list(self.settings['columns'].keys())

        df = df.rename(columns=columns)

        if self.settings['common']['adjust_time']:
            min_t = np.min(df.loc[:, 'time'])
            df.loc[:, 'time'] = df.loc[:, 'time'] - min_t

        if self.settings['common']['normalized']:
            df.loc[:, ['porx', 'pory']] = df.loc[:, ['porx', 'pory']] * np.array(self.settings['common']['resolution'])

        self.raw_df = df[cols_to_select]

    def smooth_trajectory_df(self):
        """Performs data frame coordinates smoothing with one of three (currently) methods:
        - median smoothing
        - moving average smoothing
        - Savitzky-Golay signal filtering

        :return: smoothed data frame
        :rtype: pandas.DataFrame
        """
        df = self.raw_df.copy()
        if self.settings['smoothing'] is None:
            return df
        else:
            df = df.copy()
            cols_to_smooth = df.drop('time', 1).columns
            if self.settings['smoothing']['method'] == 'savgol':
                savgol = lambda x: savgol_filter(x,
                                                 window_length=self.settings['smoothing']['window'],
                                                 polyorder=self.settings['smoothing']['order'])
                windows = df[cols_to_smooth].apply(savgol, axis=0)
            else:
                windows = df.loc[:, cols_to_smooth].rolling(window=self.settings['smoothing']['window'],
                                                            center=self.settings['smoothing']['center'])
                if self.settings['smoothing']['method'] in ['med', 'median']:
                    windows = windows.median()
                else:
                    windows = windows.mean()

            df.loc[:, cols_to_smooth] = windows
            if self.settings['smoothing']['fillna']:
                df = df.fillna(method='bfill').fillna(method='ffill')
            self.df = df

    def calculate_angular_parameters(self):
        """Performs angular parameters calculation for input coordinates data frame

        :param df: coordinates data frame
        :param settings: settings dictionary with filled common field
        :return: data frame with additional parameters
        :rtype: pandas.DataFrame
        """
        df = self.df.copy()
        d = self.settings['common']['distance']
        wid, hei = self.settings['common']['size']
        wpix, hpix = self.settings['common']['resolution']

        if self.settings['common']['reference_point'] is None:
            refx, refy = wid / 2, hei / 2
        else:
            refx, refy = self.settings['common']['reference_point']

        df['dt'] = df['time'].diff()
        # Angular coordinates
        df['xAng'] = 180 / np.pi * np.arctan((df.porx - refx) / (d * wpix / wid))
        df['yAng'] = 180 / np.pi * np.arctan((df.pory - refy) / (d * hpix / hei))
        # Angular velocity
        if self.settings['velocity']['velocity_type'] == 'finite_difference':
            df['distAng'] = np.sqrt(np.sum(df[['xAng', 'yAng']].diff() ** 2, 1))
        else:
            xdash = savgol_filter(x=df['xAng'].values,
                                  window_length=self.settings['velocity']['window'],
                                  polyorder=2,
                                  deriv=1)
            ydash = savgol_filter(x=df['yAng'].values,
                                  window_length=self.settings['velocity']['window'],
                                  polyorder=2,
                                  deriv=1)
            df['distAng'] = np.sqrt(xdash ** 2 + ydash ** 2)

        df['velAng'] = df['distAng'] / df['dt']
        df['accelAng'] = df['velAng'].diff() / df['dt']

        df.loc[:, ['velAng', 'accelAng']] = df[['velAng', 'accelAng']].replace(to_replace=[np.nan, np.inf, -np.inf],
                                                                               value=0)

        self.df = df
