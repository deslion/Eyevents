import numpy as np
import pandas as pd

from eyevents.utils import geron, graham_scan


class Summariser:
    @staticmethod
    def total_saccade_params(df, code=None, mark='Saccade'):
        """Performs basic and total saccade calculations

        :param df: events marked data frame
        :param code: code of the current trial (for several trials in experiment)
        :param mark: mark of the Saccades in the df
        :returns: two data frames - basic and total data frames
        :rtype: (pandas.DataFrame, pandas.DataFrame)
        """
        all_params = Summariser.saccade_params(df, code, mark)
        total_duration = max(df.time)
        count = len(all_params)
        horis = np.nansum(all_params.orientation == 'Horisontal')
        vertic = np.nansum(all_params.orientation == 'Vertical')

        params = dict(
            count=count,
            freq=count / total_duration,
            horis=horis, vertic=vertic,
            h_freq=horis / total_duration, v_freq=vertic / total_duration,
            mean_dur=np.nanmean(all_params.duration),
            mean_amp=np.nanmean(all_params.amplitude),
            mean_vel=np.nanmean(all_params.meanVelocity),
            code=code
        )
        total_params = pd.DataFrame(params, index=[0])
        return all_params, total_params

    @staticmethod
    def total_fixation_params(df, code=None, mark='Fixation'):
        """Performs basic and total fixations calculations

        :param df: events marked data frame
        :param code: code of the current trial (for several trials in experiment)
        :param mark: mark of the Fixations in the df
        :returns: two data frames - basic and total data frames
        :rtype: (pandas.DataFrame, pandas.DataFrame)
        """
        all_params = Summariser.fixation_params(df, code, mark)
        total_duration = max(df.time)
        count = len(all_params)

        params = dict(
            count=count,
            freq=count / total_duration,
            total_dur=np.nansum(all_params.duration),
            mean_dur=np.nanmean(all_params.duration),
            area=np.nansum(all_params.area),
            mean_area=np.nanmean(all_params.area),
            code=code
        )
        total_params = pd.DataFrame(params, index=[0])
        return all_params, total_params

    @staticmethod
    def saccade_params(df, code=None, mark='Saccade'):
        """Performs calculation of basic saccades characteristics."""
        df = df[df.event == mark].copy()
        groups = df.groupby('group')
        sac_params_funcs = [
            'nsamples',
            'duration',
            'amplitude',
            'pathLength',
            'curvature',
            'peakVelocity',
            'meanVelocity',
            'massCenterXY',
            'orientation'
        ]
        dfs = [groups.apply(getattr(Summariser, x)) for x in sac_params_funcs]
        result = pd.concat(dfs, sort=False, axis=1)
        result['code'] = code
        return result

    @staticmethod
    def fixation_params(df, code=None, mark='Fixation'):
        """Performs calculation of basic fixations characteristics."""
        df = df[df.event == mark].copy()
        groups = df.groupby('group')
        fix_params_funcs = [
            'nsamples',
            'duration',
            'massCenterXY',
            'area'
        ]
        dfs = [groups.apply(getattr(Summariser, x)) for x in fix_params_funcs]
        result = pd.concat(dfs, sort=False, axis=1)
        result['code'] = code
        return result

    @staticmethod
    def nsamples(df):
        """Calculates total samples of event. All events"""
        result = pd.Series(len(df), index=['nsamples'])
        return result

    @staticmethod
    def duration(df):
        """Calculates duration of events. Any event."""
        duration = max(df.time) - min(df.time)
        result = pd.Series(duration, index=['duration'])
        return result

    @staticmethod
    def amplitude(df):
        """Calculates angular amplitude coordinate-wise and total. Saccades only."""
        if len(df) < 2:
            amplitude_x, amplitude_y, amplitude = np.nan, np.nan, np.nan
        else:
            amplitude_x = np.abs(df.iloc[0]['xAng'] - df.iloc[-1]['xAng'])
            amplitude_y = np.abs(df.iloc[0]['yAng'] - df.iloc[-1]['yAng'])
            amplitude = np.sqrt(amplitude_x**2 + amplitude_y**2)
        result = pd.Series([amplitude_x, amplitude_y, amplitude],
                           index=['amplitudeX', 'amplitudeY', 'amplitude'])
        return result

    @staticmethod
    def pathLength(df):
        """Calculates total path length in degrees. Saccades only."""
        if len(df) < 2:
            pathLength = np.nan
        else:
            x_lines = np.abs(df.iloc[1:]['xAng'].values - df.iloc[:-1]['xAng'].values)
            y_lines = np.abs(df.iloc[1:]['yAng'].values - df.iloc[:-1]['yAng'].values)
            pathLength = np.sum(np.sqrt(x_lines**2 + y_lines**2))
        result = pd.Series(pathLength, index=['pathLength'])
        return result

    @staticmethod
    def curvature(df):
        """Calculates curvature of event. Saccades only."""
        amp = Summariser.amplitude(df)['amplitude']
        plen = Summariser.pathLength(df)['pathLength']
        if amp == 0 or plen == 0:
            curvature = np.nan
        else:
            curvature = plen / amp
        result = pd.Series(curvature, index=['curvature'])
        return result

    @staticmethod
    def peakVelocity(df):
        """Calculates peak velocity of event. Saccades only."""
        result = pd.Series(df['velAng'].max(), index=['peakVelocity'])
        return result

    @staticmethod
    def meanVelocity(df):
        """Calculates mean velocity of event. Saccades only."""
        result = pd.Series(df['velAng'].mean(), index=['meanVelocity'])
        return result

    @staticmethod
    def massCenterXY(df):
        """Calculates center of mass for all the event points. All events."""
        values = [df.xAng.mean(), df.yAng.mean()]
        result = pd.Series(values, index=['centerX', 'centerY'])
        return result

    @staticmethod
    def orientation(df):
        """Calculates the orientation of event. Saccades only."""
        x0 = df.iloc[0].xAng
        x1 = df.iloc[-1].xAng
        y0 = df.iloc[0].yAng
        y1 = df.iloc[-1].yAng
        d = (y1 - y0) / (x1 - x0)
        if d >= 2:
            orient = 'Vertical'
        elif d <= .5:
            orient = 'Horisontal'
        else:
            orient = 'Diagonal'
        result = pd.Series(orient, index=['orientation'])
        return result

    @staticmethod
    def area(df):
        """Calculates the area covered by event points. Fixations only"""
        if len(df) < 3:
            return pd.Series(np.nan, index=['area'])
        elif len(df) < 5:
            pts = list(zip(df.xAng, df.yAng))
        else:
            pts = graham_scan(list(zip(df.xAng, df.yAng)))
        area = 0
        df = pd.DataFrame(pts, columns=['x', 'y'])
        for i in range(1, len(pts)-1):
            area += geron(df.iloc[[0, i, i+1]].x.tolist(), df.iloc[[0, i, i+1]].y.tolist())
        result = pd.Series(area, index=['area'])
        return result
