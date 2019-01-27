import numpy as np


class Detector:
    @staticmethod
    def summarise_events(df):
        raise NotImplementedError()

    @staticmethod
    def group_events(df):
        """Adds group numbers for events to make futher aggregations

        :param df: input frame with detected events
        :return: df with additional 'group' column
        :rtype: pandas.DataFrame
        """
        df = df.copy()
        df.loc[:, 'event_change'] = np.concatenate([[False], np.not_equal(df.iloc[1:]['event'], df.iloc[:-1]['event'])])
        df.loc[:, 'group'] = df.event_change.cumsum() + 1
        df.drop('event_change', 1, inplace=True)
        return df

    @staticmethod
    def smooth_marks(df, window=5, center=True):
        df = df.copy()
        df['event2'] = df['event'] == 'Fixation'
        df.loc[:, 'event2'] = df['event2'].rolling(window, center=center).median()
        df = df.fillna(method='bfill').fillna(method='ffill')
        df.loc[:, 'event'] = ['Fixation' if x else 'Saccade' for x in df.event2]
        df.drop('event2', 1, inplace=True)
        return df

    @staticmethod
    def blinker(df, settings):
        """Performs blinks detection in one of several ways

        :param df: coordinates data frame
        :param settings: settings dictionary with filled filter field
        :return: data frame with additional parameters
        :rtype: pandas.DataFrame
        """
        raise NotImplementedError('This method is under construction')

    @staticmethod
    def ivt(df, settings):
        """Performs basic oculomotor events detections by velocity threshold.
        Basic events are: fixations, saccades

        :param df: coordinates data frame
        :param settings: settings dictionary with filled oculus field
        :return: data frame with additional parameters
        :rtype: pandas.DataFrame
        """
        df = df.copy()
        df['above_threshold'] = df['velAng'] > settings['oculus']['velocity_threshold']
        df['event'] = df['above_threshold'].replace([True, False], ['Saccade', 'Fixation'])
        df.drop('above_threshold', 1, inplace=True)
        df = Detector.smooth_marks(df, 5, True)
        df = Detector.group_events(df)
        return df

    @staticmethod
    def idt(df, settings):
        raise NotImplementedError('Method is under construction')

    @staticmethod
    def anh(df, settings):
        raise NotImplementedError('Method is under construction')
