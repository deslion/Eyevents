class Detector:
    @staticmethod
    def Blinker(df, settings):
        """Performs blinks detection in one of several ways

        :param df: coordinates data frame
        :param settings: settings dictionary with filled filter field
        :return: data frame with additional parameters
        :rtype: pandas.DataFrame
        """
        raise NotImplementedError('This method is under construction')

    @staticmethod
    def IVT(df, settings):
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
        return df.drop('above_threshold', 1)

    @staticmethod
    def IDT(df, settings):
        raise NotImplementedError('Method is under construction')

    @staticmethod
    def ANH(df, settings):
        raise NotImplementedError('Method is under construction')
