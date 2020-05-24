import numpy as np
import pandas as pd
from os import listdir

from eyevents.extended_trajectory import ExtendedTrajectory
from eyevents.detector import Detector
from eyevents.summariser import Summariser
from eyevents.utils import get_shortname

from tqdm import tqdm_notebook


class ExtendedTrajectories:
    def __init__(self, directory, settings=None, stimulus_pathes=None):
        """Contains trajectories with events and their parameters.

        :param directory: path to trajectory files in the same format
        :param settings: settings in proper dictionary format. You can use 'eyevent.utils.help' to see format
        :param stimulus_pathes: pathes list of stimulus files
        """
        if stimulus_pathes is None:
            raise TypeError('You should use Trajectories class.')
        if directory[-1] not in ['/', '\\']:
            directory += '/'
        files = [directory + x for x in listdir(directory)]
        shortnames = [get_shortname(x) for x in files]
        if len(stimulus_pathes) != len(shortnames):
            raise ValueError('Different lengths of files.')
        self.trajectories = {get_shortname(x): ExtendedTrajectory(x, settings, stim) for x, stim in zip(files,stimulus_pathes)}
        self.dfs = {}
        all_saccades = []
        total_saccades = []
        all_fixations = []
        total_fixations = []
        for key, val in tqdm_notebook(self.trajectories.items()):
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

        likelihoods_mask = pd.DataFrame(np.zeros((len(files), len(files))), columns=shortnames, index=shortnames)
        self.df_likelihood = likelihoods_mask.copy()
        self.df_log_likelihood = likelihoods_mask.copy()
        for row in shortnames:
            for col in shortnames:
                transitions = self.trajectories[row].transition_count
                probabilities = self.trajectories[col].transition_probability
                log_probabilities = self.trajectories[col].transition_log_probability
                self.df_likelihood.loc[row, col] = ExtendedTrajectories.get_likelihood(transitions, probabilities)
                self.df_log_likelihood.loc[row, col] = ExtendedTrajectories.get_log_likelihood(transitions, log_probabilities)

        self.df_entropies = pd.DataFrame([self.trajectories[x].entropy for x in shortnames],
                                         columns=['Entropy'], index=shortnames)
        self.df_informativities = pd.DataFrame([self.trajectories[x].informativity for x in shortnames],
                                         columns=['Informativity'], index=shortnames)

    @staticmethod
    def get_likelihood(transitions, probabilities):
        return np.product(transitions * probabilities)

    @staticmethod
    def get_log_likelihood(transitions, log_probabilities):
        return np.sum(transitions * log_probabilities)
