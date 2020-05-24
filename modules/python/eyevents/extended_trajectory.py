import numpy as np
from matplotlib import image as img

from eyevents.trajectory import Trajectory


class ExtendedTrajectory(Trajectory):
    def __init__(self, path, settings, stimulus=None):
        """Contains one trajectory values and additional parameters (velocities etc.)
        Can handle stimulus matrix for additional entropy calculation

        :param path: path to trajectory file
        :param settings: settings in proper dictionary format. You can use 'eyevent.utils.help' to see format
        :param stimulus: path to stimulus file
        """
        super().__init__(path, settings)
        self.stimulus = None
        self.informativity = None
        query = 'porx > 0 & porx < 1920 & pory > 0 & pory < 1200'
        vals = self.df.query(query)[['porx', 'pory']].astype(np.int).values
        self.x, self.y = vals[..., 0], vals[..., 1]
        self.get_stimulus_matrix(stimulus)

    def get_stimulus_matrix(self, stimulus):
        if stimulus is None:
            self.stimulus = None
            self.informativity = None
        else:
            a = img.imread(stimulus)[..., 1]
            norm = a / a.sum()
            self.stimulus = norm

            n = len(self.x)
            coords_path = []
            for x, y in zip(self.x, self.y):
                coords_path.append(self.stimulus[y][x])
            coords_path = np.array(coords_path)
            entropy = -np.sum(coords_path * np.log2(coords_path))

            bais = np.log2(n)
            self.informativity = bais - entropy
