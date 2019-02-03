import pandas as pd
from os import listdir

from eyevents.trajectory import Trajectory
from eyevents.detector import Detector
from eyevents.summariser import Summariser
from eyevents.utils import get_shortname


class Trajectories:
    def __init__(self, directory, settings=None):
        """Contains trajectories with events and their parameters.

        :param directory: path to trajectory files in the same format
        :param settings: settings in proper dictionary format. You can use 'eyevent.utils.help' to see format
        """
        if directory[-1] not in ['/', '\\']:
            directory += '/'
        files = [directory + x for x in listdir(directory)]
        self.trajectories = {get_shortname(x): Trajectory(x, settings) for x in files}
        self.dfs = {}
        all_saccades = []
        total_saccades = []
        all_fixations = []
        total_fixations = []
        for key, val in self.trajectories.items():
            detd_df = Detector.ivt(val.df, settings)
            buf_sac = Summariser.total_saccade_params(detd_df, val.name)
            buf_fix = Summariser.total_fixation_params(detd_df, val.name)
            all_saccades.append(buf_sac[0])
            total_saccades.append(buf_sac[1])
            all_fixations.append(buf_fix[0])
            total_fixations.append(buf_fix[1])
            self.dfs[key] = detd_df

        self.all_saccades = pd.concat(all_saccades, ignore_index=True)
        self.total_saccades = pd.concat(total_saccades, ignore_index=True)
        self.all_fixations = pd.concat(all_fixations, ignore_index=True)
        self.total_fixations = pd.concat(total_fixations, ignore_index=True)
