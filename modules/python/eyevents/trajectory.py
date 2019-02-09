import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from eyevents.values_checker import ValuesChecker
from eyevents.utils import get_shortname


class Trajectory:
    def __init__(self, path, settings):
        """Contains one trajectory values and additional parameters (velocities etc.)

        :param path: path to trajectory file
        :param settings: settings in proper dictionary format. You can use 'eyevent.utils.help' to see format
        """
        ValuesChecker.check_settings(settings)
        self.settings = settings.copy()
        self.path = path
        self.name = get_shortname(path)
        self.raw_df = None
        self.df = None
        self.aois_sequence = None
        self.transition_count = None
        self.transition_probability = None
        self.transition_log_probability = None
        self.get_trajectory_as_df()
        self.smooth_trajectory_df()
        self.calculate_angular_parameters()
        self.calculate_aois()
        self.get_transition_matrix()
        self.get_transition_probabilities()
        self.get_transition_log_probabilities()

    @property
    def entropy(self):
        return -np.sum(self.transition_probability * self.transition_log_probability)

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

    def calculate_aois(self):
        df = self.df.copy()

        grid = self.settings['common']['aois_grid']
        resolution = self.settings['common']['resolution']
        samples_for_step = self.settings['common']['samples_for_step']
        x_step = resolution[0] / grid[0]
        y_step = resolution[1] / grid[1]
        xs = np.concatenate([[-np.inf], np.arange(0, resolution[0] + x_step, x_step)])
        ys = np.concatenate([[-np.inf], np.arange(0, resolution[1] + y_step, y_step)])

        max_group = len(df) // samples_for_step + 1
        df['t_group'] = np.repeat(np.arange(max_group), samples_for_step)[:len(df)]
        df = df.groupby('t_group').agg({'porx':'mean', 'pory':'mean'})

        def get_aoi(x):
            x,y = x[0], x[1]
            if x<0 or x>resolution[0] or y<0 or y>resolution[1]:
                return grid[0]*grid[1]
            else:
                xp = sum(x > xs) - 1
                yp = sum(y > ys) - 1
                return (yp-1) * grid[0] + xp

        df['aoi'] = df.apply(get_aoi, axis=1)

        self.aois_sequence = df.aoi.values

    def get_transition_matrix(self):
        grid = self.settings['common']['aois_grid']
        matrix = np.zeros((grid[0]*grid[1]+1, grid[0]*grid[1]+1))
        for _from, _to in zip(self.aois_sequence[:-1], self.aois_sequence[1:]):
            matrix[_to][_from] += 1
        self.transition_count = matrix

    def get_transition_probabilities(self):
        a = self.transition_count
        b = np.sum(a, axis=0)
        matrix = np.divide(a, b, out=np.zeros_like(a), where = b!=0)
        self.transition_probability = matrix

    def get_transition_log_probabilities(self):
        a = self.transition_probability
        mask = np.ones_like(a) * -10
        matrix = np.log(a, out=mask, where = a!=0)
        self.transition_log_probability = matrix
